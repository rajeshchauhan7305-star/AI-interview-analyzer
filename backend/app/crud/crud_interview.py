from sqlalchemy.orm import Session
from app.db.models import Interview, Answer, Report
from app.schemas.question import DifficultyLevel


def create_interview(db: Session, user_id: int, category_id: int, difficulty: DifficultyLevel):
    interview = Interview(user_id=user_id, category_id=category_id, difficulty=difficulty)
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


def get_interview(db: Session, interview_id: int):
    return db.query(Interview).filter(Interview.id == interview_id).first()


def create_answer(db: Session, interview_id: int, question_id: int, text: str, analysis: dict):
    answer = Answer(
        interview_id=interview_id,
        question_id=question_id,
        text=text,
        grammar_score=analysis.get("grammar_score"),
        technical_score=analysis.get("technical_score"),
        communication_score=analysis.get("communication_score"),
        confidence_score=analysis.get("confidence_score"),
        ai_feedback=analysis.get("ai_feedback"),
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def update_interview_scores(db: Session, interview: Interview, total_score: float, summary: str, recommendation: str):
    interview.total_score = total_score
    interview.summary = summary
    interview.recommendation = recommendation
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


def create_report(db: Session, interview_id: int, pdf_path: str, overall_score: float, categories: str):
    report = Report(
        interview_id=interview_id,
        pdf_path=pdf_path,
        overall_score=overall_score,
        categories=categories,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
