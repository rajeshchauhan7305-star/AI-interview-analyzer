from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.db.models import User, Interview, Question

router = APIRouter()

@router.get("/stats")
def user_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    total_interviews = db.query(Interview).filter(Interview.user_id == current_user.id).count()
    total_questions = db.query(Question).count()
    return {
        "user": {"id": current_user.id, "name": current_user.full_name, "email": current_user.email},
        "total_interviews": total_interviews,
        "total_questions": total_questions,
    }
