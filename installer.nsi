; RepairQ Windows Installer Script (NSIS)
; Version 2.0.0

!define APP_NAME      "RepairQ"
!define APP_VERSION   "2.0.0"
!define APP_PUBLISHER "RepairQ"
!define APP_URL       "https://github.com/negoti8za/RepairQ"
!define APP_EXE       "RepairQ.exe"
!define INSTALL_DIR   "$PROGRAMFILES\${APP_NAME}"
!define UNINST_KEY    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

; ── Metadata ────────────────────────────────────────────────────
Name              "${APP_NAME} ${APP_VERSION}"
OutFile           "releases\RepairQ-Setup-v${APP_VERSION}.exe"
InstallDir        "${INSTALL_DIR}"
InstallDirRegKey  HKLM "${UNINST_KEY}" "InstallLocation"
RequestExecutionLevel admin
SetCompressor     /SOLID lzma

; ── Pages ────────────────────────────────────────────────────────
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "src\resources\icon.ico"
!define MUI_UNICON "src\resources\icon.ico"
!define MUI_WELCOMEPAGE_TEXT "This will install ${APP_NAME} v${APP_VERSION} on your computer.$\r$\n$\r$\nRepairQ is a repair shop management application for Windows.$\r$\n$\r$\nClick Next to continue."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ── Installer ────────────────────────────────────────────────────
Section "RepairQ Application" SecMain
    SectionIn RO
    SetOutPath "$INSTDIR"

    ; Copy all files from the PyInstaller onedir build
    File /r "dist\RepairQ\*.*"

    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Start Menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"     "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"       "$INSTDIR\Uninstall.exe"

    ; Desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0

    ; Registry – Add/Remove Programs
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayName"      "${APP_NAME}"
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayVersion"   "${APP_VERSION}"
    WriteRegStr   HKLM "${UNINST_KEY}" "Publisher"        "${APP_PUBLISHER}"
    WriteRegStr   HKLM "${UNINST_KEY}" "URLInfoAbout"     "${APP_URL}"
    WriteRegStr   HKLM "${UNINST_KEY}" "InstallLocation"  "$INSTDIR"
    WriteRegStr   HKLM "${UNINST_KEY}" "UninstallString"  '"$INSTDIR\Uninstall.exe"'
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayIcon"      "$INSTDIR\${APP_EXE}"
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify"         1
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair"         1
SectionEnd

; ── Uninstaller ──────────────────────────────────────────────────
Section "Uninstall"
    ; Remove installed files
    RMDir /r "$INSTDIR"

    ; Remove shortcuts
    RMDir /r "$SMPROGRAMS\${APP_NAME}"
    Delete    "$DESKTOP\${APP_NAME}.lnk"

    ; Remove registry entries
    DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd
