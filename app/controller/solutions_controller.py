from fastapi import Response, status
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from app.constants import TEMPLATES
from app.db.db_helpers import get_model_by_id
from app.model.personal_best import PersonalBest
from app.model.solution import Solution
from app.services.scramble_service import ScrambleService
from app.services.solution_service import SolutionService
from app.utils import float_to_timestr, is_valid_uuid




class SolutionsController:
    @classmethod
    def get_solutions_view(cls, puzzle: str, db: Session, cursor: str | None, limit: int = 20):
        """
        Retrieves a list of solutions for a given puzzle and returns an HTML response.

        Args:
            puzzle (str): The name of the puzzle to filter solutions by.
            db (Session): The database session.
            cursor (str | None): A cursor for pagination, defaults to None.
            limit (int): The maximum number of solutions to return, defaults to 20.

        Returns:
            HTMLResponse: A response containing the rendered HTML of the solutions.
        """

        solutions = SolutionService.get_solutions(puzzle, db, cursor, limit)

        solutions_html = []

        for solution in solutions['list']:
            solution.time = float_to_timestr(solution.time)
            html = TEMPLATES.get_template('templates/solution.html').render({
                'solution': solution
            })
            solutions_html.append(html)
        
        db.rollback()

        result_html = ''.join(solutions_html)
        
        if solutions['cursor'] is not None:
            result_html += f"""
                <li id="show-more" hx-get="/solutions?puzzle={ puzzle }&cursor={ solutions['cursor'] }" hx-target="this" hx-swap="outerHTML">Show More</li>
            """
        
        return HTMLResponse(result_html)


    @classmethod
    def create_solution(cls, solution_time: str, puzzle: str, scramble: str, db: Session):
        """
        Creates a new solution, updates the current averages, and returns an HTML response 
        with the solution, current averages, and new scramble.

        Args:
            solution_time (str): The time of the solution.
            puzzle (str): The name of the puzzle.
            scramble (str): The scramble used for the solution.
            db (Session): The database session.

        Returns:
            HTMLResponse: A response containing the rendered HTML for the solution, averages, 
            and scramble, with a status code of 201 if successful.
        """

        solution = SolutionService.create_solution(solution_time, puzzle, scramble, db)
        current_averages = SolutionService.get_current_averages(puzzle, db)
        PBs = SolutionService.get_personal_best(puzzle, db)
        trigger_UI_change = SolutionService.update_personal_best(PBs, current_averages, db)

        solution.time = float_to_timestr(solution.time)

        solution_html = TEMPLATES.get_template('templates/solution.html').render({
            'solution': solution
        })
        averages_html = TEMPLATES.get_template('templates/averages_current.html').render({
            'current_averages': current_averages,
            'puzzle': puzzle
        })
        scramble_html = TEMPLATES.get_template('templates/scramble.html').render({
            'scramble': ScrambleService.generate_scramble(puzzle)
        })

        combined_html = f"""
            {solution_html}
            <div hx-swap-oob="outerHTML:#current_averages">
                {averages_html}
            </div>
            <div hx-swap-oob="outerHTML:#scramble">
                {scramble_html}
            </div>
        """

        headers = {}
        if trigger_UI_change:
            headers["HX-Trigger"] = "new_pb"

        db.rollback()
        return HTMLResponse(combined_html, status_code=status.HTTP_201_CREATED, headers=headers)
    

    @classmethod
    def update_solution(cls, id: str, action: str, db: Session):
        """
        Updates a solution based on the provided ID and action, then returns an HTML response 
        with the updated solution.

        Args:
            id (str): The ID of the solution to update.
            action (str): The action to perform on the solution (e.g., update time, etc.).
            db (Session): The database session.

        Returns:
            HTMLResponse: A response containing the rendered HTML for the updated solution.
        """

        solution = SolutionService.update_solution(id, action, db)
        
        solution.time = float_to_timestr(solution.time)

        html = TEMPLATES.get_template('templates/solution.html').render({
            'solution': solution
        })
        headers = {'HX-Trigger': 'new_current'}
        return HTMLResponse(html, status_code=status.HTTP_200_OK, headers=headers)
    
    @classmethod
    def get_current_averages_view(cls, puzzle: str, db: Session):
        """
        Retrieves the current averages for a given puzzle and returns an HTML response.

        Args:
            puzzle (str): The name of the puzzle to get averages for.
            db (Session): The database session.

        Returns:
            HTMLResponse: A response containing the rendered HTML of the current averages.
        """

        current_averages = SolutionService.get_current_averages(puzzle, db)
        html = TEMPLATES.get_template('templates/averages_current.html').render({
            'current_averages': current_averages,
            'puzzle': puzzle
        })

        return HTMLResponse(html)
    
    @classmethod
    def get_personal_best_view(cls, puzzle: str, db: Session):
        """
        Retrieves the personal best solutions for a given puzzle and returns an HTML response.

        Args:
            puzzle (str): The name of the puzzle to get personal bests for.
            db (Session): The database session.

        Returns:
            HTMLResponse: A response containing the rendered HTML of the personal best solutions.
        """

        pbs = SolutionService.get_personal_best(puzzle, db)
        
        html = TEMPLATES.get_template('templates/averages_best.html').render({
            'personal_best': pbs,
            'puzzle': puzzle
        })

        return HTMLResponse(html)
    
    @classmethod
    def get_solution_details_view(cls, id: str, db: Session, puzzle: str | None = None):
        """
        Retrieves the details of a solution or personal best based on the provided ID and puzzle, 
        and returns an HTML response.

        Args:
            id (str): The ID of the solution or personal best to get details for.
            db (Session): The database session.
            puzzle (str | None): The puzzle to filter solutions by, defaults to None.

        Returns:
            HTMLResponse: A response containing the rendered HTML of the solution details.
            Response: A response with a 404 status if the solution ID doesn't exist.
        """
        
        template = TEMPLATES.get_template('templates/solution_details.html')

        if not is_valid_uuid(id) and puzzle is not None:
            solutions = SolutionService.get_current_averages(puzzle, db)[id]['solutions']
            details = []
            for solution in solutions:
                details.append({
                    'scramble': solution.scramble.replace('_', ' '),
                    'time_str': float_to_timestr(solution.time)
                })

            html = template.render({'details': details})
            return HTMLResponse(html)


        solution: PersonalBest | None = get_model_by_id(PersonalBest, id, db)

        if solution is not None:
            details = []
            for pb in solution.personal_bests:
                details.append({
                    'scramble': pb.solution.scramble.replace('_', ' '),
                    'time_str': float_to_timestr(pb.solution.time)
                })

            html = template.render({'details': details})
            return HTMLResponse(html)
        
        solution: Solution | None = get_model_by_id(Solution, id, db)

        if solution is None:
            return Response(content='That ID doesn\'t exist.', status_code=status.HTTP_404_NOT_FOUND)
        
        html = template.render({
            'details': [{
                'scramble': solution.scramble.replace('_', ' '),
                'time_str': float_to_timestr(solution.time)
            }]
        })
        
        return HTMLResponse(html)