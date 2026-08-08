import os
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Interview Analyzer"
    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    MYSQL_USER: str = os.getenv("MYSQL_USER", "")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "")

    SQLALCHEMY_DATABASE_URI: str = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
            if MYSQL_USER and MYSQL_SERVER and MYSQL_DB
            else "sqlite:///./backend.db"
        )
    )

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretjwt")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_PROVIDER: str = os.getenv("OPENAI_PROVIDER", "openai")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "whisper-1")

    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@aiinterview.com")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    FRONTEND_URL: str | None = os.getenv("FRONTEND_URL")
    RESUME_UPLOAD_DIR: str = os.getenv("RESUME_UPLOAD_DIR", "backend/uploads/resumes")
    PROFILE_UPLOAD_DIR: str = os.getenv("PROFILE_UPLOAD_DIR", "backend/uploads/profiles")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
