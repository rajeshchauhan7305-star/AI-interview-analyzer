from pydantic import BaseModel
from typing import Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class InterviewStart(BaseModel):
    category_id: int
    difficulty: DifficultyLevel

class InterviewAnswer(BaseModel):
    interview_id: int
    question_id: int
    answer: str

class InterviewFinish(BaseModel):
    interview_id: int
    summary: Optional[str]
    recommendation: Optional[str]

class InterviewResponse(BaseModel):
    id: int
    category_id: int
    difficulty: DifficultyLevel
    total_score: float
    summary: Optional[str]
    recommendation: Optional[str]

    class Config:
        from_attributes = True
