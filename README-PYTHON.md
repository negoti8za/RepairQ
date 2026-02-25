# RepairQ - Windows 10/11 Desktop Application

A professional repair shop management application built with **Python 3.14+** and **PyQt6**.

## Features

✅ **Modern Windows 10/11 UI** - Native PyQt6 interface
✅ **User Authentication** - Secure login with admin/user roles
✅ **Repair Management** - Track repair tickets from intake to completion
✅ **Device Management** - Catalog devices and device types
✅ **Customer Management** - Store and manage customer information
✅ **Invoice Generation** - Create and export professional invoices
✅ **Local Database** - SQLite database, offline-capable
✅ **Single Executable** - Distribute as single .exe file

## System Requirements

- **Windows 10/11** (x64)
- **No prerequisites** - Everything bundled in the executable

## Installation

### Option 1: Run Executable (Recommended for Users)

```bash
1. Download: RepairQ.exe
2. Double-click the file
3. Application starts immediately
```

### Option 2: Development Setup

```bash
# Clone repository
git clone https://github.com/negoti8za/RepairQ.git
cd RepairQ

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

## Building the Executable

```bash
# Install build tools
pip install pyinstaller

# Build single .exe
pyinstaller --onefile --windowed --name RepairQ --collect-all PyQt6 src/main.py

# Executable created in: dist/RepairQ.exe
```

Or use the provided batch file:

```bash
build.bat
```

## Default Credentials

On first launch:
- **Username:** `admin`
- **Password:** `admin`

**⚠️ Change password immediately on first login!**

## Project Structure

```
RepairQ/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── login_window.py     # Login screen
│   │   ├── main_window.py      # Main application
│   │   └── styles.py           # UI stylesheets
│   └── services/
│       ├── database.py         # SQLite operations
│       └── __init__.py
├── requirements.txt            # Python dependencies
├── setup.py                    # Build configuration
├── build.bat                   # Windows build script
├── run.bat                     # Development launcher
└── README.md                   # This file
```

## Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.14+ |
| **UI Framework** | PyQt6 | 6.7+ |
| **Database** | SQLite | 3.x |
| **Packaging** | PyInstaller | Latest |
| **OS** | Windows | 10/11 |

## Database

RepairQ uses SQLite with the following tables:

- **users** - User accounts and authentication
- **devices** - Device information
- **services** - Available services
- **repairs** - Repair tickets
- **invoices** - Invoice records
- **config** - Application configuration

Database file: `repairq.db` (stored in application directory)

## Usage

### First Launch

1. **Extract/Run** RepairQ.exe
2. **Login** with `admin`/`admin`
3. **Change Password** (required on first login)
4. **Dashboard** appears showing overview

### Main Features

#### Repairs Tab
- Create new repair tickets
- Track repair status
- Manage customer information
- Assign to technicians

#### Devices Tab
- Add device types
- Catalog devices and models
- Track serial numbers

#### Services Tab
- Define available services
- Set service descriptions and pricing

#### Invoices Tab
- Generate invoices from repairs
- Export to PDF
- Track payment status

## Troubleshooting

### Application won't start
- Ensure Windows 10+ x64
- Check that the folder structure is intact
- Verify sufficient disk space (50 MB)

### Database errors
- Delete `repairq.db` to reset
- Application will auto-recreate on next launch
- ⚠️ This will lose all data

### Performance issues
- Application uses minimal resources (~100 MB RAM)
- SQLite performs well with < 10,000 records
- For larger databases, consider migration to PostgreSQL

## Development

### Running in Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly
python src/main.py
```

### Adding Features

1. UI components: Modify files in `src/ui/`
2. Database operations: Update `src/services/database.py`
3. Business logic: Create new service files in `src/services/`

### Code Style

- Follow PEP 8
- Use type hints where practical
- Add docstrings to classes and functions

## Building for Distribution

```bash
# Create single executable
pyinstaller --onefile --windowed --name RepairQ src/main.py

# Result: dist/RepairQ.exe (standalone, ~50-60 MB)
```

## Deployment

### For System Administrators

```powershell
# Create network deployment package
# 1. Build RepairQ.exe (see above)
# 2. Distribute dist/RepairQ.exe to users
# 3. Users extract and run - no setup needed

# Deploy via Group Policy
# - Copy RepairQ.exe to network share
# - Create GPO startup script
# - Users run RepairQ.exe on first login
```

### For End Users

1. Download or receive `RepairQ.exe`
2. Double-click the file
3. Application launches
4. Login with credentials
5. Start using!

## Security

- ✅ SHA256 password hashing
- ✅ Local database (no cloud/network exposure)
- ✅ No telemetry or tracking
- ✅ Offline-capable
- ✅ User roles (Admin/Staff)

## Support

For issues or questions:
1. Check the README section above
2. Review application logs (look for error messages)
3. Delete `repairq.db` and restart to reset application state

## License

Proprietary © 2026

## Changelog

### v1.0.0 (2026-02-25)
- Initial PyQt6 version
- Complete rewrite from Java to Python
- Native Windows 10/11 UI
- Single executable distribution
- Login and authentication system
- Repair management interface
- Device and service tracking
- Invoice generation framework
