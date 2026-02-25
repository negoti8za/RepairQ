"""
RepairQ - Main Application Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtCore import Qt
from src.config import *
from src.services.database import Database
from src.services.auth import AuthService
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow


class RepairQApp(QStackedWidget):
    """Main application container"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database
        Database.initialize()
        
        # Set window properties
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Create pages
        self.login_page = LoginWindow(switch_to_main_window=self.show_main_window)
        self.main_page = None
        
        # Add pages to stack
        self.addWidget(self.login_page)
        
        # Show login
        self.setCurrentWidget(self.login_page)
    
    def show_main_window(self):
        """Switch to main window after login"""
        if self.main_page is None:
            self.main_page = MainWindow(switch_to_login=self.show_login)
            self.addWidget(self.main_page)
        
        self.setCurrentWidget(self.main_page)
    
    def show_login(self):
        """Switch back to login"""
        self.login_page = LoginWindow(switch_to_main_window=self.show_main_window)
        self.removeWidget(self.main_page)
        self.main_page = None
        
        # Recreate login page
        self.clear()
        self.login_page = LoginWindow(switch_to_main_window=self.show_main_window)
        self.addWidget(self.login_page)
        self.setCurrentWidget(self.login_page)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = RepairQApp()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
