from sqlalchemy.orm import Session
from app.db.models import Report


def get_report(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()


def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()


def get_reports_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Report).join(Report.interview).filter(Report.interview.has(user_id=user_id)).offset(skip).limit(limit).all()
