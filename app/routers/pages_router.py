from fastapi import APIRouter, Depends
from app.controller.pages_controller import PagesController
from app.db.database import get_db


router = APIRouter()


@router.get('/')
async def read_root():
    return PagesController.serve_index_file()

@router.get("/{puzzle}")
async def serve_file(puzzle: str, db = Depends(get_db)):
    return PagesController.serve_cubing_file(puzzle, db)
