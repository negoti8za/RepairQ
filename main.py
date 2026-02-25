"""
RepairQ Application Entry Point
This is the main entry point for PyInstaller bundling
"""

import sys
import os

# Ensure src package can be imported
if getattr(sys, 'frozen', False):
    # Running as packaged executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

if application_path not in sys.path:
    sys.path.insert(0, application_path)

# Now import and run the application
from src.main import main

if __name__ == "__main__":
    main()
