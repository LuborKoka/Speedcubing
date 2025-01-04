from datetime import datetime
from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import text

class PersonalBest(SQLModel, table = True):
    __tablename__ = 'personal_bests'

    id: UUID = Field(default=text('uuid_generate_v4()'), primary_key=True)
    time: float = Field(...)
    puzzle: str = Field(...)
    avg_of: int = Field(...)
    created_at: datetime = Field(default=text('NOW()'), nullable=False)

    personal_bests: list["SolutionPersonalBest"] = Relationship(back_populates="personal_best", passive_deletes=True) # type: ignore