import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
VENV_PYTHON = BACKEND_DIR / ".venv" / "bin" / "python"

if VENV_PYTHON.exists():
    python_executable = str(VENV_PYTHON)
else:
    python_executable = sys.executable
    print("Warning: backend virtual environment not found at backend/.venv. Using current Python interpreter.")
    print("If the backend dependencies are not installed, create the venv and install requirements first.")

cmd = [
    python_executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
    "--reload",
    "--log-level",
    "info",
]

print(f"Starting backend from {BACKEND_DIR} using {python_executable}")
print("Open http://0.0.0.0:8000 in your browser when the server starts.")

return_code = subprocess.call(cmd, cwd=str(BACKEND_DIR))
sys.exit(return_code)
