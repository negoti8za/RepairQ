# RepairQ Windows Application
# Modern Windows 10/11 App using Python + PyQt6

A professional repair shop management application built with:
- **Python 3.14+**
- **PyQt6** (native Windows UI framework)
- **SQLite** (local database - reusing Java schema)
- **Single .exe** Windows installer (no prerequisites)

## Project Structure

```
RepairQ/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── login_window.py     # Login interface
│   │   ├── main_window.py      # Main application window
│   │   └── styles.py           # PyQt6 stylesheets
│   ├── services/
│   │   ├── user_service.py     # User management
│   │   ├── database.py         # Database operations
│   │   └── repair_service.py   # Repair ticket management
│   ├── database/
│   │   └── repairq.db          # SQLite database
│   └── config.py               # Configuration
├── requirements.txt            # Python dependencies
├── setup.py                    # Build configuration
└── README.md
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

## Build (Windows .exe)

```bash
# Install PyInstaller
pip install pyinstaller

# Create single executable
pyinstaller --onefile --windowed --name RepairQ --icon=icon.ico src/main.py
```

## Features

- ✅ Modern Windows 10/11 native UI
- ✅ User login and authentication
- ✅ Repair ticket management
- ✅ Device tracking
- ✅ Invoice generation
- ✅ Local SQLite database
- ✅ Offline-capable
- ✅ Single .exe distribution (no prerequisites)

## Status

Converting from Java + JavaFX to Python + PyQt6 for better Windows 10/11 native integration.
