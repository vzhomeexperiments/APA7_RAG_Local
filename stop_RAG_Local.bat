@echo off
echo Stopping APA7 RAG Application...

REM Kill backend
for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv ^| findstr /i "APA7 Backend"') do taskkill /PID %%a /F

REM Kill frontend
for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv ^| findstr /i "APA7 Frontend"') do taskkill /PID %%a /F

echo Application stopped.
