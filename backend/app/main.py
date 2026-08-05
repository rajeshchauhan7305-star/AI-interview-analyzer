import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.routes import auth, users, admin, interview, questions, reports, resume, dashboard
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Interview Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/api/auth", tags=["Authentication"])
app.include_router(users, prefix="/api/users", tags=["Users"])
app.include_router(admin, prefix="/api/admin", tags=["Admin"])
app.include_router(interview, prefix="/api/interviews", tags=["Interviews"])
app.include_router(questions, prefix="/api/questions", tags=["Questions"])
app.include_router(reports, prefix="/api/reports", tags=["Reports"])
app.include_router(resume, prefix="/api/resume", tags=["Resume"])
app.include_router(dashboard, prefix="/api/dashboard", tags=["Dashboard"])

from pathlib import Path

UPLOADS_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

@app.get("/")
def root():
        frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:4173/")
        return RedirectResponse(url=frontend_url)
