@echo off
echo Starting Safe-Housing Map...

echo Installing Backend Dependencies...
"c:\Users\shlee\anaconda3\envs\ck\python.exe" -m pip install -r backend/requirements.txt

echo Installing Frontend Dependencies...
cd frontend
call npm install
cd ..

echo Starting Servers...
start "Backend" "c:\Users\shlee\anaconda3\envs\ck\python.exe" -m uvicorn backend.main:app --reload --port 8000
start "Frontend" cmd /c "cd frontend && npm run dev"

echo Done! Servers are running in background windows.
pause
