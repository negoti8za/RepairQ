@echo off
setlocal enabledelayedexpansion

REM RepairQ Application Launcher
REM Launches RepairQ using Java and the bundled JAR

cd /d "%~dp0"

REM Check if Java is available
java -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: Java is not installed or not found
    echo ==========================================
    echo.
    echo RepairQ requires Java 21 or later to run.
    echo.
    echo Please install Java 21 LTS from:
    echo https://www.oracle.com/java/technologies/downloads/
    echo.
    pause
    exit /b 1
)

echo Starting RepairQ...
echo.

REM Launch RepairQ with the fat JAR
REM Using -Xmx512m to limit max heap size
java -Xmx512m -jar "target\RepairQ-0.0.1-SNAPSHOT.jar" %*

if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: RepairQ failed to start
    echo ==========================================
    echo.
    pause
    exit /b 1
)

