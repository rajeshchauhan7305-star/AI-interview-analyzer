from sqlalchemy.orm import Session
from app.db.models import Admin


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def create_admin(db: Session, email: str, full_name: str, hashed_password: str):
    admin = Admin(email=email, full_name=full_name, hashed_password=hashed_password)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
