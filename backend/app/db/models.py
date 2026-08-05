from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class DifficultyLevel(str, enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), default="user")
    photo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user", cascade="all, delete")
    interviews = relationship("Interview", back_populates="user", cascade="all, delete")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")

class InterviewCategory(Base):
    __tablename__ = "interview_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    questions = relationship("Question", back_populates="category", cascade="all, delete")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("interview_categories.id"), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    text = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    category = relationship("InterviewCategory", back_populates="questions")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("interview_categories.id"), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_score = Column(Float, default=0.0)
    summary = Column(Text, nullable=True)
    recommendation = Column(String(255), nullable=True)

    user = relationship("User", back_populates="interviews")
    category = relationship("InterviewCategory")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete")
    report = relationship("Report", back_populates="interview", uselist=False, cascade="all, delete")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(Text, nullable=False)
    grammar_score = Column(Float, nullable=True)
    technical_score = Column(Float, nullable=True)
    communication_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    interview = relationship("Interview", back_populates="answers")
    question = relationship("Question")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    pdf_path = Column(String(500), nullable=True)
    overall_score = Column(Float, nullable=True)
    categories = Column(Text, nullable=True)

    interview = relationship("Interview", back_populates="report")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(512), nullable=True)
    succeeded = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="login_history")
