@echo off
echo Starting APA7 RAG Application...

REM === Define base project path ===
set BASE_DIR=%USERPROFILE%\Documents\GitHub\APA7_RAG_LOCAL

REM === Start Backend ===
start "APA7 Backend" cmd /k "cd /d %BASE_DIR%\backend && uv run python main.py"

REM === Start Frontend ===
start "APA7 Frontend" cmd /k "cd /d %BASE_DIR%\frontend && uv run streamlit run app.py"

echo Application started.
