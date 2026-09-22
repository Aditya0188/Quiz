@echo off
echo ====================================================
echo Starting GATE CS Quiz Master - Frontend UI
echo ====================================================
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
)
echo Starting Vite dev server at http://localhost:5173 ...
npm run dev
pause
