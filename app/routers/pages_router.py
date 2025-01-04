from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.controller.solutions_controller import SolutionsController
from app.db.database import get_db
from app.services.scramble_service import ScrambleService
from app.services.solution_service import SolutionService
from app.utils import get_cubes


templates = Jinja2Templates(directory="./app/view")

router = APIRouter()


@router.get('/')
async def read_root(req: Request):
    return templates.TemplateResponse('pages/index.html', {"request": req})

@router.get("/{subpath}")
async def serve_file(request: Request, subpath: str, db = Depends(get_db)):
    return templates.TemplateResponse('pages/cubing.html', {
        "request": request,
        "puzzle": subpath,
        "cubes": get_cubes(subpath),
        "current_averages": SolutionService.get_current_averages(subpath, db),
        "personal_best": SolutionService.get_personal_best(subpath, db),
        "scramble": ScrambleService.generate_scramble(subpath),
        "solutions": SolutionService.get_solutions(subpath, db)
    })
