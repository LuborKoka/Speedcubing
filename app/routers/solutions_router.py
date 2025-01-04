from fastapi import APIRouter, Depends, Form, Query
from sqlmodel import Session

from app.controller.solutions_controller import SolutionsController
from app.db.database import get_db
from app.services.solution_service import SolutionService

router = APIRouter()

@router.get('/solutions')
async def get_solutions(puzzle: str = Query(...), cursor: str | None = Query(None), limit: int = Query(20), db: Session = Depends(get_db)):
    return SolutionsController.get_solutions_view(puzzle, db, cursor, limit)

@router.post('/solutions')
async def create_solution(solution_time: str = Form(...), puzzle: str = Query(...), scramble: str = Form(...), db: Session = Depends(get_db)):
    return SolutionsController.create_solution(solution_time, puzzle, scramble, db)

@router.patch('/solutions')
async def update_solution(id: str = Query(...), action: str = Query(...), db: Session = Depends(get_db)):
    return SolutionsController.update_solution(id, action, db)

@router.delete('/solutions')
async def delete_solution(id: str = Query(...), db: Session = Depends(get_db)):
    return SolutionService.delete_solution(id, db)

@router.get('/solutions/current')
async def get_current_solutions(puzzle: str = Query(...), db: Session = Depends(get_db)):
    return SolutionsController.get_current_averages_view(puzzle, db)

@router.get('/solutions/best')
async def get_best_solutions(puzzle: str = Query(...), db: Session = Depends(get_db)):
    return SolutionsController.get_personal_best_view(puzzle, db)

@router.get('/solutions/details')
async def get_solution_details(id: str = Query(...), puzzle: str | None = Query(None), db: Session = Depends(get_db)):
    return SolutionsController.get_solution_details_view(id, db, puzzle)