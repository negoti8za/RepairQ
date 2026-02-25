@echo off
REM Build script for RepairQ Windows executable
REM Creates a single .exe using PyInstaller

setlocal enabledelayedexpansion

echo.
echo Building RepairQ Windows Application...
echo.

REM Install PyInstaller
echo Installing PyInstaller...
pip install -q pyinstaller

REM Create the executable
echo Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name RepairQ ^
    --distpath ".\dist" ^
    --workpath ".\build" ^
    --specpath ".\build" ^
    --console ^
    --collect-all PyQt6 ^
    src\main.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Build failed!
    echo.
    pause
    exit /b 1
)

echo.
echo SUCCESS: RepairQ.exe created in dist\ folder
echo.
echo Next steps:
echo   1. The executable is in: dist\RepairQ.exe
echo   2. You can distribute this single file to users
echo   3. Users just need to run RepairQ.exe
echo.
pause
