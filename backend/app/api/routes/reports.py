from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_current_admin
from app.crud.crud_report import get_report, get_reports, get_reports_for_user
from app.schemas.interview import InterviewResponse
from app.db.models import Report

router = APIRouter()

@router.get("/", response_model=list[dict])
def list_reports(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return [
        {"id": report.id, "interview_id": report.interview_id, "overall_score": report.overall_score, "generated_at": report.generated_at}
        for report in get_reports(db, skip=skip, limit=limit)
    ]

@router.get("/me")
def list_user_reports(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return [
        {"id": report.id, "interview_id": report.interview_id, "overall_score": report.overall_score, "generated_at": report.generated_at}
        for report in get_reports_for_user(db, current_user.id)
    ]

@router.get("/{report_id}")
def get_report_detail(report_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    report = get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return report
