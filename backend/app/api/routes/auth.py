from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin, PasswordResetRequest, PasswordResetConfirm
from app.schemas.token import Token
from app.api.deps import get_db
from app.crud.crud_user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token, create_refresh_token, get_password_hash, verify_refresh_token
from app.core.config import settings
from app.utils.email import send_email
from app.utils.token import create_email_token, verify_email_token, create_password_reset_token, verify_password_reset_token
from app.db.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(db, user_in)
    token = create_email_token(user.email)
    verification_link = f"{settings.FRONTEND_URL}verify-email?token={token}"
    email_sent = send_email(
        "Verify your email",
        user.email,
        f"<p>Hello {user.full_name},</p><p>Please verify your email by clicking <a href=\"{verification_link}\">here</a>.</p>",
        f"Hello {user.full_name},\nPlease verify your email using this link: {verification_link}",
    )

    if not email_sent:
        user.is_verified = True
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_verified = True
    db.add(user)
    db.commit()
    return {"message": "Email verified"}

@router.post("/forgot-password")
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    token = create_password_reset_token(user.email)
    reset_link = f"{settings.FRONTEND_URL}reset-password?token={token}"
    send_email(
        "Reset your password",
        user.email,
        f"<p>Hello {user.full_name},</p><p>Reset your password by clicking <a href=\"{reset_link}\">here</a>.</p>",
        f"Hello {user.full_name},\nReset your password using this link: {reset_link}",
    )
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.hashed_password = get_password_hash(request.password)
    db.add(user)
    db.commit()
    return {"message": "Password reset successful"}

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    access_token = create_access_token(subject=str(user.id))
    new_refresh = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": new_refresh, "token_type": "bearer"}
