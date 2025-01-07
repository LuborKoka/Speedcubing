from fastapi.responses import HTMLResponse
from sqlmodel import Session
from app.constants import TEMPLATES
from app.services.scramble_service import ScrambleService
from app.services.solution_service import SolutionService
from app.utils import float_to_timestr, get_cubes


class PagesController:
    @classmethod
    def serve_index_file(cls):
        html = TEMPLATES.get_template('pages/index.html').render()
        return HTMLResponse(html)

    @classmethod
    def serve_cubing_file(cls, puzzle: str, db: Session):
        current_averages = SolutionService.get_current_averages(puzzle, db)
        solutions = SolutionService.get_solutions(puzzle, db)
        for s in solutions['list']:
            s.time = float_to_timestr(s.time)


        html = TEMPLATES.get_template('pages/cubing.html').render({
            "puzzle": puzzle,
            "cubes": get_cubes(puzzle),
            "current_averages": current_averages,
            "personal_best": SolutionService.get_personal_best(puzzle, db),
            "scramble": ScrambleService.generate_scramble(puzzle),
            "solutions": solutions
        })

        db.rollback()

        return HTMLResponse(html)