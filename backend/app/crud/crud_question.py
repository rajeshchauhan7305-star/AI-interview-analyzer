from sqlalchemy.orm import Session
from app.db.models import Question, InterviewCategory, DifficultyLevel
from app.schemas.question import QuestionCreate


def create_question(db: Session, question_in: QuestionCreate):
    question = Question(
        category_id=question_in.category_id,
        text=question_in.text,
        difficulty=DifficultyLevel(question_in.difficulty.value),
        answer=question_in.answer,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()


def update_question(db: Session, question: Question, data: dict):
    for field, value in data.items():
        setattr(question, field, value)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question: Question):
    db.delete(question)
    db.commit()
    return question
