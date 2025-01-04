from typing import List
from fastapi import HTTPException, Response, status
from sqlalchemy import desc, select
from sqlmodel import Session

from app.constants import PUZZLES
from app.db.db_helpers import get_model_by_id
from app.model.personal_best import PersonalBest
from app.model.solution import Solution
from app.model.solutions_personal_best import SolutionPersonalBest
from app.types.averages import AverageDetails, CurrentAverages, CurrentPBs
from app.types.solutions import Solutions
from app.utils import float_to_timestr, get_avg_of, timestr_to_float


class SolutionService:
    @classmethod
    def get_solutions(cls, puzzle: str, db: Session, cursor: str | None = None, limit: int = 20) -> Solutions:
        """
        Retrieve a list of solutions for a specific puzzle.

        Args:
            puzzle (str): The type of puzzle for which solutions are retrieved.
            db (Session): The database session to use for querying.
            cursor (str | None): An optional cursor for pagination, representing the ID of the last retrieved solution.
            limit (int): The maximum number of solutions to retrieve. Defaults to 20.

        Returns:
            dict: A dictionary containing a list of solutions and a cursor for the next set of results.
                  If fewer than `limit` solutions are returned, the cursor will be None.

        Raises:
            HTTPException: If the specified puzzle is not supported.
        """
        if puzzle not in PUZZLES:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Puzzle {puzzle} not supported')

        statement = select(Solution).where(Solution.puzzle == puzzle).order_by(desc(Solution.created_at))

        if cursor is not None:
            cursor: Solution | None = get_model_by_id(Solution, cursor, db)
            if cursor is not None:
                statement = statement.where(Solution.created_at < cursor.created_at)

        # db.execute is deprecated and the doc says i should use "exec" method, but the exec method dont fuckin exist on the db object
        solutions: List[Solution] = db.execute(statement.limit(limit)).scalars().all()

        return {
            'list': solutions,
            'cursor': solutions[-1].id if len(solutions) == 20 else None
        }

    @classmethod
    def create_solution(cls, solution_time: str, puzzle: str, scramble: str, db: Session):
        """
        Create a new solution record in the database.

        Args:
            solution_time (str): The time taken to solve the puzzle, formatted as a string (e.g., "12.34").
            puzzle (str): The type of puzzle solved.
            scramble (str): The scramble associated with the solution.
            db (Session): The database session to use for inserting the solution.

        Returns:
            Solution: The created solution object.

        Raises:
            HTTPException: If the puzzle is not supported or the solution time format is invalid.
        """
        if puzzle not in PUZZLES:       # mozno radsej raise value error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Puzzle {puzzle} not supported')
        
        time_val = timestr_to_float(solution_time)

        if time_val is None:            # tuto mozno tiez radsej value error
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid time format')
        
        solution = Solution(time=time_val, puzzle=puzzle, scramble=scramble)
        db.add(solution)
        db.commit()
        db.refresh(solution)

        return solution
    
    @classmethod
    def update_solution(cls, id: str, action: str, db: Session):
        """
        Update an existing solution with a specific action.

        Args:
            id (str): The ID of the solution to update.
            action (str): The action to apply to the solution. Supported actions are:
                          - "penalty": Add a 2-second penalty to the solution.
                          - "dnf": Mark the solution as "Did Not Finish" (DNF).
            db (Session): The database session to use for updating the solution.

        Returns:
            Solution: The updated solution object.

        Raises:
            HTTPException: If the solution with the given ID is not found or the action is invalid.
        """
        solution: Solution | None = get_model_by_id(Solution, id, db)

        if solution is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Solution with this id was not found')
        
        if action == 'penalty':
            solution.penalty = True
            solution.time += 2

        elif action == 'dnf':
            solution.dnf = True

        else:    
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid action')
        
        db.commit()
        
        return solution
    
    @classmethod
    def delete_solution(cls, id: str, db: Session):
        """
        Delete an existing solution from the database.

        Args:
            id (str): The ID of the solution to delete.
            db (Session): The database session to use for deleting the solution.

        Returns:
            Response: An HTTP 204 No Content response to indicate successful deletion.

        Raises:
            HTTPException: If the solution with the given ID is not found.
        """
        solution: Solution | None = get_model_by_id(Solution, id, db)

        if solution is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solution with this id wasn't found.")

        db.delete(solution)
        db.commit()

        headers = {"HX-Trigger": "new_current"}
        return Response(status_code=status.HTTP_204_NO_CONTENT, headers=headers)


    @classmethod 
    def get_current_averages(cls, puzzle: str, db: Session) -> CurrentAverages:
        """
        Calculate the current averages for a specific puzzle based on the most recent solutions.

        Args:
            puzzle (str): The type of puzzle to calculate averages for.
            db (Session): The database session to use for querying.

        Returns:
            CurrentAverages: A dictionary containing the following averages:
                - "single": The fastest single time.
                - "avg_five": The average of the latest five solutions.
                - "avg_twelve": The average of the latest twelve solutions.
                - "mean_hundred": The mean of the latest hundred solutions.
        """
        statement = select(Solution).where(Solution.puzzle == puzzle).order_by(desc(Solution.created_at))
        latest: List[Solution] = db.execute(statement).scalars().all()

        mean_of_100 = get_avg_of(100, latest)
        avg_of_12 = get_avg_of(12, latest, True)
        avg_of_5 = get_avg_of(5, latest, True)
        single = get_avg_of(1, latest)

        return {
            'single': single,
            'avg_five': avg_of_5,
            'avg_twelve': avg_of_12,
            'mean_hundred': mean_of_100
        }
    
    @classmethod
    def get_personal_best(cls, puzzle: str, db: Session) -> CurrentPBs:
        """
        Retrieve the personal bests (PBs) for a specific puzzle.

        Args:
            puzzle (str): The type of puzzle to retrieve personal bests for.
            db (Session): The database session to use for querying.

        Returns:
            CurrentPBs: A dictionary containing the personal bests for:
                - "single": The fastest single time.
                - "avg_five": The best average of five solutions.
                - "avg_twelve": The best average of twelve solutions.
                - "mean_hundred": The best mean of a hundred solutions.
              Each entry includes the PB object and a time string representation.
        """
        statement = select(PersonalBest).where(PersonalBest.puzzle == puzzle)
        PBs: List[PersonalBest] = db.execute(statement).scalars().all()

        pbs_dict = {
            pb.avg_of: pb for pb in PBs
        }

        return {
            "single": {
                'pb': pbs_dict.get(1),
                'time_str': float_to_timestr(pbs_dict.get(1).time if pbs_dict.get(1) else None)
            },
            "avg_five":  {
                'pb': pbs_dict.get(5),
                'time_str': float_to_timestr(pbs_dict.get(5).time if pbs_dict.get(5) else None)
            },
            "avg_twelve":  {
                'pb': pbs_dict.get(12),
                'time_str': float_to_timestr(pbs_dict.get(12).time if pbs_dict.get(12) else None)
            },
            "mean_hundred":  {
                'pb': pbs_dict.get(100),
                'time_str': float_to_timestr(pbs_dict.get(100).time if pbs_dict.get(100) else None)
            }
        }
    
    @classmethod
    async def set_new_personal_best(cls, old: PersonalBest, new: AverageDetails, db: Session):
        """
        Set a new personal best (PB) for a specific puzzle and update the database.

        Args:
            old (PersonalBest): The current personal best to be replaced. Can be None if no PB exists.
            new (AverageDetails): The new average details to set as the personal best.
            db (Session): The database session to use for updating the database.

        Returns:
            PersonalBest: The newly created personal best record.
        """
        puzzle = new['solutions'][0].puzzle
        avg_of = len(new['solutions'])

        if old is not None:
            db.delete(old)

        pb = PersonalBest(time=new['time'], puzzle=puzzle, avg_of=avg_of)
        db.add(pb)
        db.commit()
        db.refresh(pb)

        for solution in new['solutions']:
            item = SolutionPersonalBest(solution=solution, personal_best=pb)
            db.add(item)

        db.commit()
        return pb
    

    @classmethod
    def update_personal_best(cls, pbs: CurrentPBs, current: CurrentAverages, db: Session):
        """
        Update personal bests for a specific puzzle if current averages are better.

        Args:
            pbs (CurrentPBs): The existing personal bests for the puzzle.
            current (CurrentAverages): The current averages calculated from the latest solutions.
            db (Session): The database session to use for updating the database.

        Returns:
            bool: True if any personal best was updated (triggering a UI change), otherwise False.
        """
        trigger_UI_change = False
        for key, value in current.items():
            if value['time'] is None:
                continue

            if pbs[key]['pb'] is None or pbs[key]['pb'].time > value['time']:            # if current avg is better than PB
                cls.set_new_personal_best(pbs[key]['pb'], value, db)
                trigger_UI_change = True

        return trigger_UI_change