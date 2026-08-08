from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.crud.crud_user import update_user
from app.utils.file import save_upload, allowed_image
from app.core.config import settings

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = user_update.dict(exclude_unset=True)
    updated_user = update_user(db, current_user, data)
    return updated_user

@router.post("/me/photo")
def upload_profile_photo(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not allowed_image(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")
    path = save_upload(settings.PROFILE_UPLOAD_DIR, file, prefix=f"user_{current_user.id}_")
    current_user.photo_url = path
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"photo_url": path}

@router.get("/history")
def get_interview_history(current_user=Depends(get_current_user)):
    return {"message": "Use /api/interviews/history for interview history."}
