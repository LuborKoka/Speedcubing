from typing import List, TypedDict
from app.model.personal_best import PersonalBest
from app.model.solution import Solution

class AverageDetails(TypedDict):
    time_str: str
    time: float | None
    solutions: List[Solution] | None

class CurrentAverages(TypedDict):
    single: AverageDetails
    avg_five: AverageDetails
    avg_twelve: AverageDetails
    mean_hundred: AverageDetails

class PersonalBestDetails(TypedDict):
    pb: PersonalBest
    time_str: str

class CurrentPBs(TypedDict):
    single: PersonalBestDetails
    avg_five: PersonalBestDetails
    avg_twelve: PersonalBestDetails
    mean_hundred: PersonalBestDetails