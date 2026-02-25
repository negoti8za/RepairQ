@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM   RepairQ Desktop Application - Self-Contained Launcher
REM   Zero Prerequisites: Java 21 is bundled - just run this file!
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Path to bundled Java runtime
set JAVA_HOME=%SCRIPT_DIR%\jre
set JAVA_EXE=%JAVA_HOME%\bin\java.exe

REM Log file for debugging
set LOG_FILE=%SCRIPT_DIR%\RepairQ-run.log

REM ─────────────────────────────────────────────────────────────────────────
REM Verify bundled Java exists
REM ─────────────────────────────────────────────────────────────────────────
if not exist "%JAVA_EXE%" (
    echo. >> "%LOG_FILE%"
    echo [%date% %time%] ERROR: Bundled Java not found >> "%LOG_FILE%"
    echo [%date% %time%] Expected at: %JAVA_EXE% >> "%LOG_FILE%"
    
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║           RepairQ - INSTALLATION ERROR                   ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo ERROR: RepairQ installation is incomplete.
    echo.
    echo The bundled Java runtime was not found at:
    echo   %JAVA_EXE%
    echo.
    echo SOLUTION: Re-extract the RepairQ distribution ZIP file.
    echo.
    pause
    exit /b 1
)

REM ─────────────────────────────────────────────────────────────────────────
REM Build classpath (JAR + all libs)
REM ─────────────────────────────────────────────────────────────────────────
set JAR_FILE=%SCRIPT_DIR%\RepairQ-0.0.1-SNAPSHOT.jar

if not exist "%JAR_FILE%" (
    echo [%date% %time%] ERROR: JAR file not found >> "%LOG_FILE%"
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║           RepairQ - INSTALLATION ERROR                   ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo ERROR: RepairQ JAR not found at:
    echo   %JAR_FILE%
    echo.
    echo SOLUTION: Re-extract the RepairQ distribution ZIP file.
    echo.
    pause
    exit /b 1
)

REM Build dynamic classpath with all JARs
set CLASSPATH=%JAR_FILE%
for %%F in ("%SCRIPT_DIR%\libs\*.jar") do (
    set CLASSPATH=!CLASSPATH!;%%F
)

echo [%date% %time%] Starting RepairQ >> "%LOG_FILE%"
echo [%date% %time%] Java: %JAVA_EXE% >> "%LOG_FILE%"
echo [%date% %time%] JAR: %JAR_FILE% >> "%LOG_FILE%"
echo [%date% %time%] Classpath entries: %SCRIPT_DIR%\libs (36 JARs) >> "%LOG_FILE%"

REM ─────────────────────────────────────────────────────────────────────────
REM Launch RepairQ with bundled Java
REM ─────────────────────────────────────────────────────────────────────────
"%JAVA_EXE%" -cp "%CLASSPATH%" -Xmx512m com.zoran_jankov.repairq.app.RepairQ 2>&1 | tee -a "%LOG_FILE%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║           RepairQ - STARTUP ERROR                        ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo ERROR: RepairQ failed to start (Error code: %ERRORLEVEL%)
    echo.
    echo Check the log file for details:
    echo   %LOG_FILE%
    echo.
    pause
    exit /b 1
)

echo [%date% %time%] RepairQ exited normally >> "%LOG_FILE%"
exit /b 0
