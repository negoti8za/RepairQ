"""
Main Window - Application interface with responsive layout
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QMenuBar, QMenu, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction
from src.config import *
from src.services.auth import AuthService
from src.utils.logger import AppLogger
from src.ui.pages.dashboard import DashboardPage
from src.ui.pages.repairs import RepairsPage
from src.ui.pages.customers import CustomersPage
from src.ui.pages.devices import DevicesPage
from src.ui.pages.invoices import InvoicesPage
from src.ui.pages.admin_panel import AdminPanel


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, switch_to_login=None):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.init_ui()
    
    def init_ui(self):
        """Initialize main window with error handling"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setStyleSheet(self._get_stylesheet())
        
        try:
            # Create menu bar
            self._create_menu_bar()
            
            # Create status bar
            self._create_status_bar()
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Main layout
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)
            
            # Header with user info
            header = self._create_header()
            main_layout.addWidget(header)
            
            # Tabbed interface
            self.tabs = QTabWidget()
            self.tabs.setStyleSheet(self._get_tab_stylesheet())
            
            # Add pages with error handling
            try:
                self.dashboard_page = DashboardPage()
                self.tabs.addTab(self.dashboard_page, "Dashboard")
            except Exception as e:
                print(f"Error loading dashboard: {e}")
                self.tabs.addTab(QWidget(), "Dashboard (Error)")
            
            try:
                self.repairs_page = RepairsPage()
                self.tabs.addTab(self.repairs_page, "Repair Tickets")
            except Exception as e:
                print(f"Error loading repairs: {e}")
                self.tabs.addTab(QWidget(), "Repair Tickets (Error)")
            
            try:
                self.customers_page = CustomersPage()
                self.tabs.addTab(self.customers_page, "Customers")
            except Exception as e:
                print(f"Error loading customers: {e}")
                self.tabs.addTab(QWidget(), "Customers (Error)")
            
            try:
                self.devices_page = DevicesPage()
                self.tabs.addTab(self.devices_page, "Devices")
            except Exception as e:
                print(f"Error loading devices: {e}")
                self.tabs.addTab(QWidget(), "Devices (Error)")
            
            try:
                self.invoices_page = InvoicesPage()
                self.tabs.addTab(self.invoices_page, "Invoices")
            except Exception as e:
                print(f"Error loading invoices: {e}")
                self.tabs.addTab(QWidget(), "Invoices (Error)")
            
            # Add admin panel if user is admin
            try:
                user = AuthService.get_current_user()
                print(f"[MainWindow] get_current_user returned: {user}")
                if user:
                    print(f"[MainWindow] User role: {user.get('role')}")
                    print(f"[MainWindow] is_admin() returns: {AuthService.is_admin()}")
                    if user.get('role') == 'ADMIN' or AuthService.is_admin():
                        print(f"[MainWindow] Creating AdminPanel...")
                        try:
                            self.admin_panel = AdminPanel()
                            self.tabs.addTab(self.admin_panel, "Admin Panel")
                            print("[MainWindow] Admin panel loaded successfully")
                        except Exception as admin_error:
                            print(f"[MainWindow] AdminPanel creation failed: {admin_error}")
                            import traceback
                            traceback.print_exc()
                            self.tabs.addTab(QWidget(), "Admin Panel (Error)")
                    else:
                        print(f"[MainWindow] User is not admin. Role: {user.get('role')}")
                else:
                    print(f"[MainWindow] No user data available")
            except Exception as e:
                print(f"[MainWindow] Error loading admin panel: {e}")
                import traceback
                traceback.print_exc()
            
            main_layout.addWidget(self.tabs, 1)
            central_widget.setLayout(main_layout)
        except Exception as e:
            print(f"Critical error in main window initialization: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _create_header(self) -> QWidget:
        """Create header with user info and tools"""
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLOR_PRIMARY}; padding: 10px 15px;")
        header.setMaximumHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # App title
        title = QLabel(APP_NAME)
        title_font = QFont(FONT_FAMILY, FONT_SIZE_NORMAL, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # User info
        user = AuthService.get_current_user()
        user_info = QLabel(f"User: {user.get('first_name', 'User')} ({user.get('role', 'STAFF')})")
        user_font = QFont(FONT_FAMILY, FONT_SIZE_SMALL)
        user_info.setFont(user_font)
        user_info.setStyleSheet("color: white;")
        layout.addWidget(user_info)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setMaximumWidth(100)
        logout_btn.setMinimumHeight(30)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.3);
            }}
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def _create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        menubar.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About RepairQ", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _create_status_bar(self):
        """Create status bar"""
        status_bar = QStatusBar()
        status_bar.setFont(QFont(FONT_FAMILY, FONT_SIZE_SMALL))
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")
    
    def handle_logout(self):
        """Handle logout"""
        AuthService.logout()
        self.switch_to_login()
    

    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Modern Repair Shop Management System\n\n"
            "Originally developed by Zoran Jankov\n"
            "Enhanced and modernized by Robert Visser\n\n"
            "This is an open-source fork dedicated to improving\n"
            "repair shop operations and customer service.")
    
    def _get_stylesheet(self) -> str:
        """Get stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {COLOR_BACKGROUND};
            }}
            QWidget {{
                background-color: {COLOR_BACKGROUND};
                color: {COLOR_TEXT_PRIMARY};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}pt;
            }}
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border: none;
                padding: 5px 12px;
                font-weight: bold;
                border-radius: 3px;
                min-width: 65px;
            }}
            QPushButton:hover {{
                background-color: #005a9e;
            }}
            QPushButton:pressed {{
                background-color: #004080;
            }}
            QPushButton:disabled {{
                background-color: #aaa;
                color: #ddd;
            }}
            QPushButton[danger="true"] {{
                background-color: {COLOR_DANGER};
            }}
            QPushButton[danger="true"]:hover {{
                background-color: #a00620;
            }}
            QMenuBar {{
                background-color: {COLOR_BACKGROUND};
                border-bottom: 1px solid {COLOR_BORDER};
            }}
            QMenuBar::item:selected {{
                background-color: {COLOR_SURFACE};
            }}
            QMenu {{
                background-color: {COLOR_BACKGROUND};
                border: 1px solid {COLOR_BORDER};
            }}
            QMenu::item:selected {{
                background-color: {COLOR_SURFACE};
            }}
            QStatusBar {{
                background-color: {COLOR_SURFACE};
                border-top: 1px solid {COLOR_BORDER};
            }}
        """
    
    def _get_tab_stylesheet(self) -> str:
        """Get tab stylesheet"""
        return f"""
            QTabWidget::pane {{
                border: 1px solid {COLOR_BORDER};
            }}
            QTabBar::tab {{
                background-color: {COLOR_SURFACE};
                color: {COLOR_TEXT_PRIMARY};
                padding: 8px 20px;
                margin-right: 2px;
                border: 1px solid {COLOR_BORDER};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {COLOR_BACKGROUND};
                border-bottom: 2px solid {COLOR_PRIMARY};
            }}
            QTabBar::tab:hover {{
                background-color: #E8E8E8;
            }}
        """
