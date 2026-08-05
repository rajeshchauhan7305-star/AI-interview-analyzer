import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings


def save_upload(directory: str, upload_file: UploadFile, prefix: str = "") -> str:
    Path(directory).mkdir(parents=True, exist_ok=True)
    extension = Path(upload_file.filename).suffix
    filename = f"{prefix}{int(Path(upload_file.filename).stat().st_mtime if Path(upload_file.filename).exists() else 0)}_{upload_file.filename}".replace(" ", "_")
    path = Path(directory) / filename
    with path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return str(path)


def allowed_resume(filename: str) -> bool:
    return filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")


def allowed_image(filename: str) -> bool:
    return filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png")
