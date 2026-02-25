# RepairQ Desktop Application

## ✅ Installation - Zero Prerequisites

RepairQ comes with everything you need. **No installation required beyond extracting the files.**

### Quick Start:
1. **Extract** the `RepairQ-Windows-v1.0.zip` file to any folder
2. **Double-click** `RepairQ-Run.bat`
3. **Login** with default credentials:
   - Username: `admin`
   - Password: `admin`
4. Change your password immediately (you'll be prompted)

That's it! ✓

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| **Windows** | Windows 10 or later (x64) |
| **Disk Space** | ~150 MB for application + Java runtime |
| **RAM** | 512 MB minimum (1 GB recommended) |
| **Installation** | **NONE** - Everything is included |

---

## What's Included

```
RepairQ-Windows-v1.0/
├── RepairQ-Run.bat              ← Click this to launch
├── RepairQ-0.0.1-SNAPSHOT.jar   ← Application (39 MB)
├── jre/                          ← Java 21 Runtime (46 MB, bundled)
├── libs/                         ← All dependencies (36 JARs)
│   ├── javafx-*.jar             ← UI framework
│   ├── sqlite-jdbc-*.jar        ← Database driver
│   ├── hibernate-*.jar          ← ORM framework
│   └── (32 more dependencies)
└── README.md                     ← This file
```

---

## Features

### Repair Tickets
- Create, update, and track repair tickets
- Assign to technicians
- Track status and priority
- Customer information management

### Inventory
- Manage devices, device types, and models
- Track services and service types
- Maintain status and priority levels

### Users & Roles
- Admin: Full access to system
- Staff/Technician: Restricted access
- Secure password management

### Reporting
- Generate professional invoices
- Customizable branding (logo, company info)
- PDF export capability

### Local & Offline
- All data stored locally in SQLite database
- Works completely offline
- No internet connection required
- Your data stays on your computer

---

## First-Time Setup

On first launch, RepairQ will:
1. Create default `admin` user (password: `admin`)
2. Initialize the local database
3. Create necessary configuration files

**Important:** Change the default admin password immediately after first login.

---

## Troubleshooting

### App won't start
1. Verify Windows 10+ (x64) is installed
2. Check that the entire folder structure is intact
3. Check `RepairQ-run.log` for error details
4. Try re-extracting the ZIP file

### "Java not found" error
- The bundled Java is included; this shouldn't happen
- Try re-extracting the complete distribution folder
- Ensure `jre` folder exists alongside `RepairQ-Run.bat`

### Database errors
- Delete `repairq.db` file to start fresh (you'll lose data)
- Restart the application
- The database will be recreated automatically

### Performance issues
- The line `java -Xmx512m` in `RepairQ-Run.bat` limits memory to 512 MB
- If you have sufficient RAM, you can increase it:
  - Edit `RepairQ-Run.bat`
  - Change `-Xmx512m` to `-Xmx1024m` (1 GB) or higher

---

## Updating RepairQ

To update to a newer version:
1. Download the new `RepairQ-Windows-v{version}.zip`
2. Extract to a new folder
3. Copy your existing `repairq.db` file from the old folder to the new folder
4. Use the new `RepairQ-Run.bat`

---

## Uninstalling

Simply delete the RepairQ folder. No registry entries or system-wide installation.

---

## Support & Documentation

- **Database Location**: `repairq.db` (in the application folder)
- **Configuration**: Settings stored in database tables
- **Logs**: `RepairQ-run.log` (in the application folder)

---

## Technical Details

- **Language**: Java 21 LTS
- **UI Framework**: JavaFX 21
- **Database**: SQLite 3
- **Architecture**: None / Local-first design
- **Licensing**: Proprietary

---

**RepairQ v1.0** - Built for simplicity and reliability.
