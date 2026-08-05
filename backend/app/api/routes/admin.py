from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.admin import AdminLogin, AdminResponse
from app.schemas.dashboard import AdminStatsResponse
from app.api.deps import get_db, get_current_admin
from app.crud.crud_admin import get_admin_by_email
from app.crud.crud_user import get_user, get_user_by_email, deactivate_user
from app.crud.crud_question import get_questions
from app.crud.crud_category import get_categories
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.db.models import User, Interview

router = APIRouter()

@router.post("/login")
def admin_login(form_data: AdminLogin, db: Session = Depends(get_db)):
    admin = get_admin_by_email(db, form_data.email)
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    return {"access_token": create_access_token(subject=str(admin.id)), "refresh_token": create_refresh_token(subject=str(admin.id)), "token_type": "bearer"}

@router.get("/stats", response_model=AdminStatsResponse)
def admin_stats(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_interviews = db.query(Interview).count()
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_interviews": total_interviews,
        "total_questions": len(get_questions(db, 0, 1000)),
    }

@router.post("/users/{user_id}/block")
def block_user(user_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    db.add(user)
    db.commit()
    return {"message": "User blocked"}

@router.post("/users/{user_id}/unblock")
def unblock_user(user_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    db.add(user)
    db.commit()
    return {"message": "User unblocked"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
