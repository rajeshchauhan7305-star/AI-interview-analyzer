import os
import signal
import shutil
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
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


def _start_frontend(host: str, port: int):
    if not FRONTEND_DIR.exists():
        print("Frontend folder not found; skipping frontend startup.")
        return None

    npm_executable = shutil.which("npm")
    if npm_executable is None:
        print("npm not found; frontend will not be started automatically.")
        return None

    frontend_port = port
    if not _is_port_free(host, frontend_port):
        try:
            frontend_port = _find_free_port(preferred=frontend_port, host=host, max_tries=20)
            print(f"Frontend port {port} is in use; selected free port {frontend_port}.")
        except RuntimeError as exc:
            print(str(exc))
            return None

    cmd = [npm_executable, "run", "dev", "--", "--host", host, "--port", str(frontend_port)]
    proc = subprocess.Popen(cmd, cwd=str(FRONTEND_DIR), stdout=sys.stdout, stderr=sys.stderr)
    return proc, frontend_port


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

backend_port = preferred_port
if not _is_port_free("0.0.0.0", backend_port):
    try:
        backend_port = _find_free_port(preferred=backend_port, host="0.0.0.0", max_tries=100)
        print(f"Port {preferred_port} is in use; selected free port {backend_port}.")
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

frontend_port = int(os.environ.get("FRONTEND_PORT", "4173"))
frontend_host = os.environ.get("FRONTEND_HOST", "0.0.0.0")
frontend_url = os.environ.get("FRONTEND_URL", f"http://127.0.0.1:{frontend_port}/")

frontend_process = _start_frontend(frontend_host, frontend_port)
if frontend_process is not None:
    proc, actual_frontend_port = frontend_process
    if "FRONTEND_URL" not in os.environ:
        frontend_url = f"http://127.0.0.1:{actual_frontend_port}/"
        os.environ["FRONTEND_URL"] = frontend_url
    print(f"Starting frontend at {frontend_url}")
    print("Opening the frontend in your browser...")
    time.sleep(1)
    try:
        webbrowser.open(frontend_url)
    except Exception as exc:
        print(f"Could not open browser automatically: {exc}")

cmd = [
    python_executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    str(backend_port),
    "--reload",
    "--log-level",
    "info",
]

print(f"Starting backend from {BACKEND_DIR} using {python_executable}")
print(f"Open http://0.0.0.0:{backend_port} in your browser when the server starts.")

try:
    return_code = subprocess.call(cmd, cwd=str(BACKEND_DIR))
finally:
    if frontend_process is not None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

sys.exit(return_code)
