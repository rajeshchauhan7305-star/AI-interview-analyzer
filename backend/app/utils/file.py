import shutil
import time
import uuid
from pathlib import Path
from fastapi import UploadFile


def save_upload(directory: str, upload_file: UploadFile, prefix: str = "") -> str:
    Path(directory).mkdir(parents=True, exist_ok=True)
    extension = Path(upload_file.filename).suffix
    timestamp = int(time.time() * 1000)
    unique_id = uuid.uuid4().hex[:8]
    safe_name = Path(upload_file.filename).stem.replace(" ", "_")
    filename = f"{prefix}{safe_name}_{timestamp}_{unique_id}{extension}"
    path = Path(directory) / filename
    with path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return str(path)


def allowed_resume(filename: str) -> bool:
    return filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")


def allowed_image(filename: str) -> bool:
    return filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png")
