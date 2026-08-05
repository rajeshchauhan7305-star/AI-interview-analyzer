from pydantic import BaseModel
from typing import Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class QuestionBase(BaseModel):
    category_id: int
    text: str
    difficulty: DifficultyLevel
    answer: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    category_id: Optional[int]
    text: Optional[str]
    difficulty: Optional[DifficultyLevel]
    answer: Optional[str]

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True
