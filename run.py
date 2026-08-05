import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
VENV_PYTHON = BACKEND_DIR / ".venv" / "bin" / "python"


def _is_port_free(host: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.close()
        return True
    except OSError:
        return False


def _find_free_port(preferred: int = 8000, host: str = "0.0.0.0", max_tries: int = 100) -> int:
    port = preferred
    for _ in range(max_tries):
        if _is_port_free(host, port):
            return port
        port += 1
    raise RuntimeError(f"No free port found starting at {preferred} after {max_tries} attempts")


if VENV_PYTHON.exists():
    python_executable = str(VENV_PYTHON)
else:
    python_executable = sys.executable
    print("Warning: backend virtual environment not found at backend/.venv. Using current Python interpreter.")
    print("If the backend dependencies are not installed, create the venv and install requirements first.")

# Prefer environment variables if provided
env_port = os.environ.get("BACKEND_PORT") or os.environ.get("PORT")
try:
    preferred_port = int(env_port) if env_port else 8000
except ValueError:
    print(f"Invalid port in BACKEND_PORT/PORT: {env_port!r}, falling back to 8000")
    preferred_port = 8000

port = preferred_port
if not _is_port_free("0.0.0.0", port):
    try:
        port = _find_free_port(preferred=preferred_port, host="0.0.0.0", max_tries=100)
        print(f"Port {preferred_port} is in use; selected free port {port}.")
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

cmd = [
    python_executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    str(port),
    "--reload",
    "--log-level",
    "info",
]

print(f"Starting backend from {BACKEND_DIR} using {python_executable}")
print(f"Open http://0.0.0.0:{port} in your browser when the server starts.")

return_code = subprocess.call(cmd, cwd=str(BACKEND_DIR))
sys.exit(return_code)
