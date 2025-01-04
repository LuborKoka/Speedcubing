from datetime import datetime
from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import text

from app.model.personal_best import PersonalBest
from app.model.solution import Solution

class SolutionPersonalBest(SQLModel, table = True):
    __tablename__ = 'solutions_personal_bests'

    id: UUID = Field(default=text('uuid_generate_v4()'), primary_key=True)
    created_at: datetime = Field(default=text('NOW()'), nullable=False)
    solution_id: UUID = Field(foreign_key='solutions.id')
    personal_best_id: UUID = Field(foreign_key='personal_bests.id')

    solution: Solution = Relationship(back_populates="solutions")
    personal_best: PersonalBest = Relationship(back_populates="personal_bests")