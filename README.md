# AI-interview-analyzer

A full-stack AI Interview Analyzer application with React + Vite + Tailwind CSS frontend and FastAPI + SQLAlchemy backend.

## How to run

### Backend

1. Open a terminal and go to the backend folder:
   ```bash
   cd /workspaces/AI-interview-analyzer/backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment example and update values if needed:
   ```bash
   cp .env.example .env
   ```
5. Start MySQL and create the database from `backend/schema.sql` if not already created.
6. Run the FastAPI server:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend

1. Open a terminal and go to the frontend folder:
   ```bash
   cd /workspaces/AI-interview-analyzer/frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

### Access

- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Frontend: use the Vite URL shown in terminal, typically `http://localhost:4173`
