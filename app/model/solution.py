from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import text
from datetime import datetime

class Solution(SQLModel, table = True):
    __tablename__ = 'solutions'

    id: UUID = Field(default=text('uuid_generate_v4()'), primary_key=True)
    time: float = Field(...)
    penalty: bool = Field(default=False)
    dnf: bool = Field(default=False)
    puzzle: str = Field(...)
    scramble: str = Field(...)
    created_at: datetime = Field(default=text('NOW()'))

    solutions: list["SolutionPersonalBest"] = Relationship(back_populates="solution", passive_deletes=True) # type: ignore

    class Config:
        arbitrary_types_allowed = True