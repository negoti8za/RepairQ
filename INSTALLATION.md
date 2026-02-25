# RepairQ Windows Installer

## Installation Instructions

### System Requirements
- **Operating System:** Windows 10 or later (64-bit)
- **RAM:** Minimum 512 MB (1 GB recommended)
- **Storage:** At least 500 MB of free disk space
- **Java:** Built-in (Java Runtime included with application)

### Installation Steps

#### Option 1: Automated Installer (Recommended)
1. Extract the **RepairQ-Installer.zip** file to any location
2. Right-click on **RepairQ-Install.bat** 
3. Select **"Run as administrator"**
4. Follow the on-screen prompts
5. The application will be installed to `C:\Program Files\RepairQ`
6. A shortcut will be created in the Start Menu and optionally on the Desktop

#### Option 2: Portable Installation
If you prefer a portable version (no installation required):
1. Extract the **RepairQ-Portable.zip** file to your desired location
2. Navigate to the extracted folder
3. Double-click **RepairQ.exe** to launch the application
4. No Start Menu or Desktop shortcuts will be created

### Launching RepairQ

After installation, you can launch RepairQ by:
- **Start Menu:** Click Start → All Programs → RepairQ → RepairQ
- **Desktop Shortcut:** Double-click the RepairQ icon on your desktop
- **Command Line:** Navigate to `C:\Program Files\RepairQ\RepairQ` and run `RepairQ.exe`

### Uninstallation

To uninstall RepairQ:
1. **Method 1 (Recommended):** Go to Start Menu → All Programs → RepairQ → Uninstall RepairQ
2. **Method 2 (Manual):** 
   - Open File Explorer
   - Navigate to `C:\Program Files\RepairQ`
   - Delete the entire **RepairQ** folder
   - Remove shortcuts from Start Menu if desired

### Troubleshooting

#### Application Won't Start
- Ensure Windows 10 or later is installed
- Try running from elevated Command Prompt: `cd "C:\Program Files\RepairQ\RepairQ" && RepairQ.exe`
- Check that administrator privileges were used during installation

#### Installation Failed
- Ensure you have administrator privileges
- Check that you have sufficient disk space (500 MB minimum)
- Try disabling antivirus temporarily during installation
- Ensure the installation script is not blocked by Windows (Right-click → Properties → Unblock if present)

#### Database Issues
- The application stores data in a local SQLite database (`repairq.db`)
- The database is automatically created on first launch
- To reset the database, delete `repairq.db` from the application directory (requires restart)

### Features

RepairQ is a desktop application designed for repair shops with the following features:
- **Ticket Management:** Track and manage repair tickets
- **Device Registry:** Keep records of devices being repaired
- **User Management:** Manage staff with role-based access
- **Offline Capability:** Works completely offline - no internet required
- **Windows Integrated:** Native Windows application with Start Menu integration

### System Details

- **Version:** 1.0
- **Platform:** Windows (64-bit)
- **Technology Stack:** Java 21, JavaFX, SQLite
- **Distribution Format:** Self-contained (includes Java Runtime)

### Support

For issues, feature requests, or questions:
- Visit: https://github.com/negoti8za/RepairQ
- Report issues on the GitHub repository

### License

RepairQ is provided as-is for repair shop management.

---

**Important:** The application includes a built-in Java runtime and will run independently of any system Java installation.
