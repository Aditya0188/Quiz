@echo off
echo ====================================================
echo Launching GATE CS Quiz Master (Full-Stack)
echo ====================================================
echo.
echo 1. Launching Backend on http://localhost:8000 ...
start "GATE Quiz Backend (FastAPI)" cmd /k "cd /d %~dp0 && call run_backend.bat"

echo 2. Launching Frontend on http://localhost:5173 ...
start "GATE Quiz Frontend (React + Vite)" cmd /k "cd /d %~dp0 && call run_frontend.bat"

echo.
echo ====================================================
echo Both servers are starting!
echo Open your browser at: http://localhost:5173
echo ====================================================
timeout /t 3 >nul
start http://localhost:5173
