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
        # Friendly HTML landing page that links to the frontend dev server
        frontend_url = "http://127.0.0.1:4173/"
        html = f"""
        <!doctype html>
        <html>
            <head>
                <meta charset='utf-8'/>
                <meta name='viewport' content='width=device-width,initial-scale=1'/>
                <title>AI Interview Analyzer</title>
                <style>body{{font-family:system-ui,Segoe UI,Roboto,-apple-system,Arial;margin:40px;background:#0f172a;color:#e6eef8}}a{{color:#7dd3fc}}</style>
            </head>
            <body>
                <h1>AI Interview Analyzer API is running</h1>
                <p>Backend is healthy. Open the frontend at <a href='{frontend_url}'>{frontend_url}</a></p>
                <p>If you're running the frontend on a different port, update the URL accordingly.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html)
