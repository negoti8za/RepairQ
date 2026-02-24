@echo off
REM RepairQ Application Launcher for Windows
REM This launcher requires Java 21+ to be installed on the system

setlocal enabledelayedexpansion

REM Get the directory where this script is located
cd /d "%~dp0"

REM Create a log file to track execution
set LOGFILE=RepairQ-run.log
echo [%date% %time%] Starting RepairQ launcher... > "%LOGFILE%"

REM Check if Java is installed
echo [%date% %time%] Checking for Java installation... >> "%LOGFILE%"
java -version >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo  ERROR: Java is not installed or not in system PATH
    echo ============================================================
    echo.
    echo  RepairQ requires Java 21 LTS or later
    echo.
    echo  Please install Java 21 from one of these sources:
    echo  1. Oracle JDK: https://www.oracle.com/java/technologies/downloads/
    echo  2. OpenJDK: https://openjdk.org/
    echo  3. Temurin (Eclipse): https://adoptium.net/
    echo.
    echo  After installation, restart your computer and try again.
    echo.
    pause
    exit /b 1
)

REM Verify the JAR exists
if not exist "RepairQ-0.0.1-SNAPSHOT.jar" (
    echo.
    echo ============================================================
    echo  ERROR: RepairQ JAR file not found!
    echo ============================================================
    echo.
    echo  Expected file: RepairQ-0.0.1-SNAPSHOT.jar
    echo  Current directory: %cd%
    echo.
    pause
    exit /b 1
)

echo [%date% %time%] Java is available. Starting RepairQ application...  >> "%LOGFILE%"
echo Starting RepairQ...
echo.

REM Run the application
REM Parameters:
REM -Xmx512m          : Maximum heap size of 512 MB
REM -Djava.awt.headless=false : Enable GUI (default)
echo [%date% %time%] Executing: java -Xmx512m -jar "RepairQ-0.0.1-SNAPSHOT.jar" >> "%LOGFILE%"
java -Xmx512m -jar "RepairQ-0.0.1-SNAPSHOT.jar" %* >> "%LOGFILE%" 2>&1

if errorlevel 1 (
    echo.
    echo ============================================================
    echo  ERROR: RepairQ failed to start (Exit Code: %ERRORLEVEL%)
    echo ============================================================
    echo.
    echo  Check the log file: %LOGFILE%
    echo.
    type "%LOGFILE%"
    echo.
    pause
    exit /b 1
)

echo [%date% %time%] RepairQ closed successfully >> "%LOGFILE%"
exit /b 0

