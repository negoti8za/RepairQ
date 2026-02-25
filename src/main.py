#!/usr/bin/env python3
"""
RepairQ - Windows 10/11 Desktop Application
Main entry point for the application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from services.database import Database


def main():
    """Initialize and run the RepairQ application"""
    
    # Initialize database
    Database.initialize()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("RepairQ")
    app.setApplicationVersion("1.0.0")
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
