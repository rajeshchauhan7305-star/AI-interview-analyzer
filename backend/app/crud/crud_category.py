from sqlalchemy.orm import Session
from app.db.models import InterviewCategory
from app.schemas.category import CategoryCreate


def get_category(db: Session, category_id: int):
    return db.query(InterviewCategory).filter(InterviewCategory.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InterviewCategory).offset(skip).limit(limit).all()


def create_category(db: Session, category_in: CategoryCreate):
    category = InterviewCategory(name=category_in.name, description=category_in.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: InterviewCategory, data: dict):
    for field, value in data.items():
        setattr(category, field, value)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: InterviewCategory):
    db.delete(category)
    db.commit()
    return category
