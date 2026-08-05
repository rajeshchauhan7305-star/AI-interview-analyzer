from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.interview import InterviewStart, InterviewAnswer, InterviewFinish, InterviewResponse
from app.crud.crud_interview import create_interview, create_answer, update_interview_scores, get_interview
from app.crud.crud_question import get_questions, get_question
from app.services.ai_service import analyze_answer, transcribe_audio
from app.services.report_service import generate_pdf_report
from app.db.models import InterviewCategory
from pathlib import Path
from app.core.config import settings
import tempfile

router = APIRouter()

@router.post("/start")
def start_interview(interview_in: InterviewStart, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    interview = create_interview(db, current_user.id, interview_in.category_id, interview_in.difficulty)
    questions = db.query(InterviewCategory).filter(InterviewCategory.id == interview_in.category_id).first().questions
    if not questions:
        questions = get_questions(db, skip=0, limit=5)
    return {"interview_id": interview.id, "questions": [{"id": q.id, "text": q.text, "difficulty": q.difficulty.value} for q in questions[:5]]}

@router.post("/answer")
def save_answer(answer_in: InterviewAnswer, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    interview = get_interview(db, answer_in.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    question = get_question(db, answer_in.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    analysis = analyze_answer(answer_in.answer, question.text)
    saved = create_answer(db, interview.id, question.id, answer_in.answer, analysis)
    return saved

@router.post("/transcribe")
def transcribe_audio_file(file: UploadFile = File(...)):
    temp_dir = Path(tempfile.mkdtemp())
    file_path = temp_dir / file.filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())
    transcript = transcribe_audio(str(file_path))
    return {"transcript": transcript}

@router.post("/finish")
def finish_interview(finish_in: InterviewFinish, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    interview = get_interview(db, finish_in.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    total = sum([answer.grammar_score or 0 + answer.technical_score or 0 + answer.communication_score or 0 + answer.confidence_score or 0 for answer in interview.answers])
    count = len(interview.answers) * 4
    overall = round(total / count, 2) if count else 0
    summary = finish_in.summary or "Interview completed."
    recommendation = finish_in.recommendation or ("Selected" if overall >= 75 else "Needs Improvement")
    update_interview_scores(db, interview, overall, summary, recommendation)
    report_path = Path(settings.RESUME_UPLOAD_DIR).parent / "reports" / f"interview_{interview.id}.pdf"
    report_data = {
        "user_name": current_user.full_name,
        "category": interview.category.name if interview.category else "N/A",
        "difficulty": interview.difficulty.value,
        "overall_score": overall,
        "recommendation": recommendation,
        "summary": summary,
    }
    generate_pdf_report(str(report_path), report_data)
    return {"interview_id": interview.id, "report_path": str(report_path), "overall_score": overall, "recommendation": recommendation}

from app.db.models import Interview

@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    interviews = db.query(Interview).filter(Interview.user_id == current_user.id).all()
    return [{"id": i.id, "category_id": i.category_id, "difficulty": i.difficulty.value, "total_score": i.total_score, "recommendation": i.recommendation, "created_at": i.created_at} for i in interviews]

@router.get("/{interview_id}")
def get_interview_details(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    interview = get_interview(db, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview
