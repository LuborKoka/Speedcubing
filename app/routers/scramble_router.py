from fastapi import APIRouter, Query
from fastapi.templating import Jinja2Templates

from app.controller.scramble_controller import ScrambleController


router = APIRouter()


templates = Jinja2Templates(directory="./app/view")

@router.get('/scramble')
async def create_scramble(puzzle: str = Query(...)):
    return ScrambleController.get_scramble_view(puzzle)

