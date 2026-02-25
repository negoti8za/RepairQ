# RepairQ Windows Distribution - Build Summary

**Build Date:** February 24, 2026  
**Version:** 1.0  
**Platform:** Windows 64-bit  
**Java Version:** Java 21 LTS (Bundled)

## Distribution Packages

### 1. RepairQ-Installer-v1.0.zip (52.78 MB)
**Recommended for most users**

This package includes:
- `RepairQ/` - The complete application with bundled Java runtime
- `RepairQ-Install.bat` - Automated Windows installer script
- `INSTALLATION.md` - Detailed installation instructions
- `README.md` - Project information

**Installation:**
1. Extract the ZIP file
2. Right-click `RepairQ-Install.bat`
3. Select "Run as administrator"
4. Follow the on-screen prompts
5. Application installs to: `C:\Program Files\RepairQ`

**Advantages:**
- Professional installer experience
- Start Menu integration
- Desktop shortcuts
- Automatic uninstaller
- No technical knowledge required

---

### 2. RepairQ-Portable-v1.0.zip (52.78 MB)
**For portable/temporary installations**

This package includes:
- `RepairQ/` - The complete application ready to run

**Usage:**
1. Extract the ZIP file to any location
2. Navigate to the extracted folder
3. Double-click `RepairQ.exe` to launch
4. No installation or admin rights needed
5. Run from USB drives or external storage

**Advantages:**
- No installation required
- Can run from any location
- Portable (USB drives, external disks)
- No system modifications
- Easy to uninstall (just delete folder)

---

## Build Details

### Technology Stack
- **Java:** Java 21 LTS
- **Framework:** JavaFX 21
- **Database:** SQLite 3.45.1.0
- **Build Tool:** Maven 3.9.x
- **Packaging Tool:** jpackage (included with JDK 21)

### Application Contents

The `RepairQ/` folder contains:
- `RepairQ.exe` - Windows application launcher
- `runtime/` - Embedded Java 21 runtime environment  
- `app/` - Application JAR and resources
- Total size: ~150 MB (includes Java runtime)
- Total files: ~445 files

### Installation Options

```
RepairQ provides TWO installation methods:

┌─────────────────────────────────────────┐
│ Option 1: Installer (Recommended)       │
├─────────────────────────────────────────┤
│ • Extract ZIP                           │
│ • Run RepairQ-Install.bat (Admin)       │
│ • Automatic Start Menu shortcuts        │
│ • System-integrated installation        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Option 2: Portable (No Installation)    │
├─────────────────────────────────────────┤
│ • Extract ZIP to any location           │
│ • Run RepairQ/RepairQ.exe directly      │
│ • No admin rights required              │
│ • Easy cleanup (delete folder)          │
└─────────────────────────────────────────┘
```

### System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| OS | Windows 10 (64-bit) | Windows 10/11 (64-bit) |
| RAM | 512 MB | 1 GB |
| Storage | 500 MB free | 1 GB free |
| CPU | 1 GHz | 2 GHz+ |
| Internet | None (Offline capable) | Optional (updates) |

**Note:** Java runtime is bundled - no separate Java installation needed!

---

## Build Artifacts

### Generated During Compilation

1. **JAR File**
   - `RepairQ-0.0.1-SNAPSHOT.jar` (in `target/` folder)
   - Contains compiled application code

2. **App-Image (jpackage)**
   - `RepairQ/` folder
   - Windows executable with bundled Java runtime
   - Ready-to-run application directory

3. **Distribution Packages**
   - `RepairQ-Installer-v1.0.zip` - Professional installer (52.78 MB)
   - `RepairQ-Portable-v1.0.zip` - Portable version (52.78 MB)

---

## Features Included

✓ Cross-platform Java 21 application
✓ Native Windows desktop integration
✓ Offline-first capability
✓ SQLite database (local storage)
✓ User authentication with BCrypt hashing
✓ JavaFX modern UI framework
✓ Bundled Java runtime (no JDK required)
✓ Comprehensive installer with uninstall support

---

## First-Time Setup

When RepairQ launches for the first time:

1. **Database Initialization**
   - SQLite database created automatically
   - Initial schema setup performed

2. **Default Admin User**
   - Username: `admin`
   - Password: `admin`
   - Users must change password on first login

3. **Features Available**
   - Ticket management
   - Device registry
   - User management with roles
   - Branding configuration
   - Invoice customization

---

## Technical Information

### Compilation Process

```powershell
# 1. Clean build
mvn clean compile

# 2. Package JAR
mvn package -DskipTests

# 3. Create app-image with jpackage
jpackage --type app-image \
  --name RepairQ \
  --input target \
  --main-jar RepairQ-0.0.1-SNAPSHOT.jar \
  --main-class com.repairq.app.RepairQ \
  --app-version 1.0
```

### Distribution Package Creation

```powershell
# Create Installer ZIP
Compress-Archive -Path @("RepairQ", "RepairQ-Install.bat", "INSTALLATION.md", "README.md") `
  -DestinationPath "RepairQ-Installer-v1.0.zip"

# Create Portable ZIP
Compress-Archive -Path "RepairQ" `
  -DestinationPath "RepairQ-Portable-v1.0.zip"
```

---

## Verification Checklist

- [x] Java 21 compilation successful
- [x] All dependencies resolved (no CVEs)
- [x] Code audit completed
- [x] Unit tests compiled
- [x] Maven package created (JAR built)
- [x] jpackage app-image generated
- [x] Windows app-image includes:
  - [x] RepairQ.exe launcher
  - [x] Bundled Java 21 runtime
  - [x] All application resources
  - [x] SQLite database library
  - [x] JavaFX libraries
- [x] Installer script created
- [x] Documentation provided
- [x] Distribution ZIPs created

---

## Next Steps

### For Users
1. Download one of the ZIP packages
2. Extract to a location of your choice
3. Run installer or execute RepairQ.exe directly
4. Launch application
5. Log in with default credentials (if first time)

### For Developers
- Source code: [GitHub](https://github.com/negoti8za/RepairQ)
- To rebuild: `mvn clean package`
- To modify: Edit source in `src/main/java/com/repairq/`
- To test: Run unit tests with `mvn test`

---

## Support & Documentation

- **Installation Help:** See `INSTALLATION.md`
- **Project Info:** See `README.md`
- **Issues/Bugs:** GitHub Issues
- **Source Code:** [negoti8za/RepairQ](https://github.com/negoti8za/RepairQ)

---

**Built with ❤️ using modern Java technologies**  
RepairQ Desktop Application v1.0 | Windows 64-bit Edition
