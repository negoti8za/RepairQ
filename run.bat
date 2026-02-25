@echo off
REM RepairQ - Windows Application Launcher
REM This batch file launches the Python application

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10+ from https://www.python.org
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -q PyQt6

REM Run the application
python src\main.py
