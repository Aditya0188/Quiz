@echo off
echo ====================================================
echo Starting GATE CS Quiz Master - Backend Server
echo ====================================================
cd /d "%~dp0backend"
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
    .venv\Scripts\python seed_db.py
)
echo Starting FastAPI server at http://localhost:8000 ...
.venv\Scripts\uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
