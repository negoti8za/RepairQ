@echo off
REM RepairQ Windows Installer Script
REM This script installs RepairQ to the user's Program Files directory

setlocal enabledelayedexpansion

REM Colors for output (using Windows 10+ ANSI escape codes)
for /F %%A in ('copy /Z "%~f0" nul') do set "BS=%%A"

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :hasAdmin
) else (
    echo RepairQ Installer
    echo.
    echo This installer requires administrator privileges.
    echo Please run this script as Administrator.
    echo.
    pause
    exit /b 1
)

:hasAdmin
cls
echo.
echo ============================================================
echo         RepairQ - Desktop Application Installer
echo ============================================================
echo.
echo Version: 1.0
echo.

REM Define installation paths
set "INSTALL_DIR=%ProgramFiles%\RepairQ"
set "START_MENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\RepairQ"
set "SHORTCUT_TARGET=%INSTALL_DIR%\RepairQ\RepairQ.exe"

echo Installation Path: %INSTALL_DIR%
echo.

REM Ask user for confirmation
echo Do you want to install RepairQ to %INSTALL_DIR%?
echo.
set /p PROCEED="Continue? (Y/N): "
if /i not "%PROCEED%"=="Y" (
    echo Installation cancelled.
    pause
    exit /b 0
)

echo.
echo Installing RepairQ...
echo.

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo Created installation directory
)

REM Copy application files
echo Copying application files...
xcopy /E /I /Y "RepairQ" "%INSTALL_DIR%\RepairQ" >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Failed to copy application files
    pause
    exit /b 1
)
echo Application files copied successfully

REM Create Start Menu shortcut
echo Creating Start Menu shortcuts...
if not exist "%START_MENU%" mkdir "%START_MENU%"

REM Create shortcut using PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; " ^
    "$shortcut = $ws.CreateShortcut('%START_MENU%\RepairQ.lnk'); " ^
    "$shortcut.TargetPath = '%SHORTCUT_TARGET%'; " ^
    "$shortcut.WorkingDirectory = '%INSTALL_DIR%\RepairQ'; " ^
    "$shortcut.IconLocation = '%SHORTCUT_TARGET%, 0'; " ^
    "$shortcut.Save()" ^
    >nul 2>&1

REM Create Desktop shortcut
echo Creating Desktop shortcut...
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if "%VERSION%" geq "10.0" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "$ws = New-Object -ComObject WScript.Shell; " ^
        "$shortcut = $ws.CreateShortcut('%UserProfile%\Desktop\RepairQ.lnk'); " ^
        "$shortcut.TargetPath = '%SHORTCUT_TARGET%'; " ^
        "$shortcut.WorkingDirectory = '%INSTALL_DIR%\RepairQ'; " ^
        "$shortcut.IconLocation = '%SHORTCUT_TARGET%, 0'; " ^
        "$shortcut.Save()" ^
        >nul 2>&1
)

REM Create uninstaller
echo Creating uninstaller...
(
    @echo @echo off
    @echo REM RepairQ Uninstaller
    @echo setlocal
    @echo.
    @echo echo Uninstalling RepairQ...
    @echo.
    @echo REM Remove installation directory
    @echo rmdir /s /q "%INSTALL_DIR%" 2>nul
    @echo.
    @echo REM Remove Start Menu shortcuts
    @echo rmdir /s /q "%START_MENU%" 2>nul
    @echo.
    @echo REM Remove Desktop shortcut
    @echo del /q "%%UserProfile%%\Desktop\RepairQ.lnk" 2>nul
    @echo.
    @echo echo RepairQ has been uninstalled successfully.
    @echo pause
) > "%START_MENU%\Uninstall RepairQ.bat"

echo.
echo ============================================================
echo        Installation Complete!
echo ============================================================
echo.
echo RepairQ has been installed successfully.
echo.
echo The application can be launched from:
echo  - Start Menu: All Programs ^> RepairQ
echo  - Desktop Shortcut (if created^)
echo  - Direct Path: %INSTALL_DIR%\RepairQ\RepairQ.exe
echo.
echo To uninstall RepairQ in the future:
echo  - Go to Start Menu ^> RepairQ ^> Uninstall RepairQ
echo  - OR manually delete the folder: %INSTALL_DIR%
echo.
pause
exit /b 0
