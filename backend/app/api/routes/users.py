from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.crud.crud_user import update_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = user_update.dict(exclude_unset=True)
    updated_user = update_user(db, current_user, data)
    return updated_user

@router.get("/history")
def get_interview_history(current_user=Depends(get_current_user)):
    return {"message": "Use /api/interviews/history for interview history."}
