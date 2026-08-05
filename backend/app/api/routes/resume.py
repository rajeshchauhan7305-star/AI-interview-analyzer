from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.utils.file import save_upload, allowed_resume
from app.db.models import Resume
from app.schemas.user import UserResponse
from app.crud.crud_user import update_user
from app.db.models import User

router = APIRouter()

@router.post("/upload")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not allowed_resume(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid resume format")
    path = save_upload("backend/uploads/resumes", file, prefix=f"user_{current_user.id}_")
    resume = Resume(user_id=current_user.id, file_path=path)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {"message": "Resume uploaded", "resume_id": resume.id, "file_path": resume.file_path}

@router.get("/me")
def get_resume(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")
    return resume
