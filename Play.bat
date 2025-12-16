@echo off
setlocal
cd /d "%~dp0"

REM Check Python launcher
where py >nul 2>nul
if errorlevel 1 (
  echo Python (py launcher) not found. Install Python from python.org and try again.
  pause
  exit /b 1
)

REM Create venv if missing
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
)

REM Upgrade pip + install project
.venv\Scripts\python.exe -m pip install -U pip >nul
.venv\Scripts\python.exe -m pip install -e . >nul

REM Run the app (package-relative imports work)
.venv\Scripts\python.exe -m src.main

pause
endlocal
