@echo off
echo ========================================================
echo Starting IPL Akinator (Backend + Frontend)
echo ========================================================

start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 2 >nul
start cmd /k "cd frontend && npm run dev"

echo Services are launching!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo ========================================================
pause
