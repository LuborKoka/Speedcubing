from typing import List, TypedDict

from app.model.solution import Solution

class Solutions(TypedDict):
    list: List[Solution]
    cursor: str | None