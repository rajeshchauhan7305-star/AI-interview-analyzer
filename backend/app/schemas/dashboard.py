from pydantic import BaseModel

class AdminStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_interviews: int
    total_questions: int

    class Config:
        from_attributes = True
