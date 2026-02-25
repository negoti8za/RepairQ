@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM RepairQ Application Launcher for Windows
REM ============================================================
REM This launcher supports multiple execution modes:
REM 1. Using fat JAR (if only JAR exists)
REM 2. Using classpath with separate JARs (if libs folder exists)
REM ============================================================

cd /d "%~dp0"

REM Create log file
set LOGFILE=%~dp0RepairQ-run.log
echo [%date% %time%] Starting RepairQ launcher... > "%LOGFILE%"

REM Check if Java is available
echo [%date% %time%] Checking for Java installation... >> "%LOGFILE%"
java -version >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo  ERROR: Java 21 LTS is not installed or not in PATH
    echo ============================================================
    echo.
    echo  Please install Java 21 LTS from:
    echo  https://adoptium.net/temurin/releases/
    echo.
    echo  OR add Java to your PATH environment variable
    echo.
    pause
    exit /b 1
)

REM Verify JAR file exists
if not exist "RepairQ-0.0.1-SNAPSHOT.jar" (
    echo.
    echo ============================================================
    echo  ERROR: RepairQ JAR file not found!
    echo ============================================================
    echo.
    echo  Expected file: RepairQ-0.0.1-SNAPSHOT.jar
    echo  Location: %cd%
    echo.
    pause
    exit /b 1
)

REM Determine execution mode
set "EXEC_MODE=1"
set "CP=RepairQ-0.0.1-SNAPSHOT.jar"

if exist "libs" (
    REM Mode 2: Use libs folder with classpath
    echo [%date% %time%] Found libs folder - using modular classpath... >> "%LOGFILE%"
    set "EXEC_MODE=2"
    setlocal enabledelayedexpansion
    set "CP=RepairQ-0.0.1-SNAPSHOT.jar"
    
    for /f "delims=" %%f in ('dir /b "libs\*.jar" 2^>nul') do (
        set "CP=!CP!;libs\%%f"
    )
    endlocal & set "CP=%CP%"
) else (
    echo [%date% %time%] Using fat JAR mode... >> "%LOGFILE%"
)

REM Launch RepairQ
echo [%date% %time%] Executing RepairQ (Mode !EXEC_MODE!)... >> "%LOGFILE%"
echo.
echo ============================================================
echo  RepairQ - Repair Shop Management System
echo ============================================================
echo.
echo Launching application... (this may take 5-10 seconds)
echo.

REM Execute with proper classpath and module configuration
java -Xmx512m ^
    -Dfile.encoding=UTF-8 ^
    -cp "%CP%" ^
    com.repairq.app.RepairQ >> "%LOGFILE%" 2>&1

set "EXIT_CODE=%ERRORLEVEL%"

if %EXIT_CODE% neq 0 (
    echo.
    echo ============================================================
    echo  ERROR: RepairQ failed with exit code %EXIT_CODE%
    echo ============================================================
    echo.
    echo Check the log file for details:
    echo  %LOGFILE%
    echo.
    type "%LOGFILE%"
    echo.
    pause
    exit /b %EXIT_CODE%
)

echo [%date% %time%] RepairQ closed successfully >> "%LOGFILE%"
exit /b 0


