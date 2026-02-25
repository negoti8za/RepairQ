"""
RepairQ - Main Application Entry Point
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.config import *
from src.services.database import Database
from src.services.auth import AuthService
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow
from src.utils.logger import AppLogger


class RepairQApp(QStackedWidget):
    """Main application container"""
    
    def __init__(self):
        super().__init__()
        
        try:
            AppLogger.info("Initializing RepairQ application...")
            
            # Initialize database
            Database.initialize()
            AppLogger.info("Database initialized successfully")
            
            # Set window properties
            self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
            self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
            
            # Set window icon
            self._set_window_icon()
            
            # Create pages
            self.login_page = LoginWindow(switch_to_main_window=self.show_main_window)
            self.main_page = None
            
            # Add pages to stack
            self.addWidget(self.login_page)
            
            # Show login
            self.setCurrentWidget(self.login_page)
            
            AppLogger.info("RepairQ application initialized successfully")
        except Exception as e:
            AppLogger.exception(f"Error initializing application: {e}")
            raise
    
    def _set_window_icon(self):
        """Set window icon - handles both dev mode and PyInstaller frozen EXE"""
        import sys
        icon_paths = []
        # Check PyInstaller extracted temp directory first
        if hasattr(sys, '_MEIPASS'):
            meipass = Path(sys._MEIPASS)
            icon_paths += [
                meipass / "resources" / "icon.ico",
                meipass / "icon.ico",
            ]
        # Dev mode paths
        icon_paths += [
            Path("src/resources/icon.ico"),
            Path("resources/icon.ico"),
            Path("src/resources/images/logo.ico"),
            Path("resources/images/logo.ico"),
            Path("icon.ico"),
        ]

        for icon_path in icon_paths:
            if icon_path.exists():
                try:
                    icon = QIcon(str(icon_path))
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        AppLogger.info(f"Window icon loaded from {icon_path}")
                        return
                except Exception as e:
                    AppLogger.warning(f"Failed to load icon from {icon_path}: {e}")

        AppLogger.debug("No icon file found - using default window icon")
    
    def show_main_window(self):
        """Switch to main window after login"""
        try:
            if self.main_page is None:
                AppLogger.info("Loading main window...")
                self.main_page = MainWindow(switch_to_login=self.show_login)
                self.addWidget(self.main_page)
                AppLogger.info("Main window loaded successfully")
            
            self.setCurrentWidget(self.main_page)
        except Exception as e:
            AppLogger.exception(f"Error loading main window: {e}")
            raise
    
    def show_login(self):
        """Switch back to login"""
        try:
            AppLogger.info("User logged out - returning to login page")
            if self.main_page is not None:
                self.removeWidget(self.main_page)
                self.main_page = None
            
            # Recreate login page
            self.login_page = LoginWindow(switch_to_main_window=self.show_main_window)
            self.addWidget(self.login_page)
            self.setCurrentWidget(self.login_page)
            AppLogger.info("Login page displayed")
        except Exception as e:
            AppLogger.exception(f"Error returning to login: {e}")
            raise


def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        AppLogger.info("="*60)
        AppLogger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        AppLogger.info(f"Python: {sys.version}")
        AppLogger.info(f"Working Directory: {os.getcwd()}")
        AppLogger.info("="*60)
        
        # Create and show main window
        window = RepairQApp()
        window.show()
        AppLogger.info("Application window displayed")
        
        # Run application
        sys.exit(app.exec())
    
    except Exception as e:
        AppLogger.critical(f"Fatal application error: {e}")
        AppLogger.exception("Stack trace:")
        raise


if __name__ == "__main__":
    main()
