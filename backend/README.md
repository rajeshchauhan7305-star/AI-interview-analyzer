# AI Interview Analyzer Backend

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy `.env.example` to `.env` and update values.
4. Ensure MySQL is running and create the database named in `MYSQL_DB`.
5. Start the backend:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API

The backend exposes OpenAPI docs at `http://localhost:8000/docs`.

## Notes

- Uses JWT access/refresh authentication.
- Uses OpenAI for question generation and answer analysis.
- Stores uploaded resumes in `backend/uploads/resumes`.
