from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_current_admin
from app.crud.crud_question import get_question, get_questions, create_question, update_question, delete_question
from app.crud.crud_category import get_categories, get_category, create_category, update_category, delete_category
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.ai_service import generate_interview_questions

router = APIRouter()

@router.get("/", response_model=list[QuestionResponse])
def list_questions(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_questions(db, skip=skip, limit=limit)

@router.post("/generate")
def generate_questions(category: str, difficulty: str = "Easy", count: int = 5):
    return {"questions": generate_interview_questions(category, difficulty, count)}

@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@router.post("/", response_model=QuestionResponse)
def create_new_question(question_in: QuestionCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_question(db, question_in)

@router.put("/{question_id}", response_model=QuestionResponse)
def edit_question(question_id: int, question_update: QuestionUpdate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    question = get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return update_question(db, question, question_update.dict(exclude_unset=True))

@router.delete("/{question_id}")
def remove_question(question_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    question = get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    delete_question(db, question)
    return {"message": "Question deleted"}

@router.post("/categories", response_model=CategoryResponse)
def create_new_category(category_in: CategoryCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_category(db, category_in)

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def edit_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return update_category(db, category, category_update.dict(exclude_unset=True))

@router.delete("/categories/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    delete_category(db, category)
    return {"message": "Category deleted"}
