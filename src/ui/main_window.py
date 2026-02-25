"""
Main window - PyQt6 UI for RepairQ application after login
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton, QLabel, QTableWidget,
                             QTableWidgetItem, QMenuBar, QMenu, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.styles import get_stylesheet
from services.database import Database


class MainWindow(QMainWindow):
    """Main application window for RepairQ"""
    
    def __init__(self, user_info: dict):
        super().__init__()
        self.user_info = user_info
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main window UI"""
        self.setWindowTitle(f"RepairQ - {self.user_info['username']}")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Set stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Create menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("RepairQ - Repair Shop Management")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        user_label = QLabel(f"Logged in as: {self.user_info['username']}")
        user_label.setFont(QFont("Arial", 10))
        header_layout.addWidget(user_label)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Tabs
        self.tabs = QTabWidget()
        self.create_tabs()
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
    
    def create_tabs(self):
        """Create tabs for different sections"""
        
        # Dashboard tab
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout()
        dashboard_label = QLabel("Dashboard - Overview of Repair Shop Operations")
        dashboard_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        dashboard_layout.addWidget(dashboard_label)
        dashboard_layout.addStretch()
        dashboard_tab.setLayout(dashboard_layout)
        self.tabs.addTab(dashboard_tab, "Dashboard")
        
        # Repairs tab
        repairs_tab = self.create_repairs_tab()
        self.tabs.addTab(repairs_tab, "Repairs")
        
        # Devices tab
        devices_tab = self.create_devices_tab()
        self.tabs.addTab(devices_tab, "Devices")
        
        # Services tab
        services_tab = self.create_services_tab()
        self.tabs.addTab(services_tab, "Services")
        
        # Invoices tab
        invoices_tab = self.create_invoices_tab()
        self.tabs.addTab(invoices_tab, "Invoices")
    
    def create_repairs_tab(self) -> QWidget:
        """Create repairs management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Button bar
        button_layout = QHBoxLayout()
        add_btn = QPushButton("+ New Repair")
        add_btn.clicked.connect(lambda: self.show_message("New Repair", "Feature coming soon"))
        button_layout.addWidget(add_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Customer", "Device", "Status", "Date"])
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        
        tab.setLayout(layout)
        return tab
    
    def create_devices_tab(self) -> QWidget:
        """Create devices management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Button bar
        button_layout = QHBoxLayout()
        add_btn = QPushButton("+ New Device")
        add_btn.clicked.connect(lambda: self.show_message("New Device", "Feature coming soon"))
        button_layout.addWidget(add_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Device Type", "Brand", "Model", "Serial"])
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        
        tab.setLayout(layout)
        return tab
    
    def create_services_tab(self) -> QWidget:
        """Create services management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Button bar
        button_layout = QHBoxLayout()
        add_btn = QPushButton("+ New Service")
        add_btn.clicked.connect(lambda: self.show_message("New Service", "Feature coming soon"))
        button_layout.addWidget(add_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Service Name", "Description"])
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        
        tab.setLayout(layout)
        return tab
    
    def create_invoices_tab(self) -> QWidget:
        """Create invoices management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Button bar
        button_layout = QHBoxLayout()
        add_btn = QPushButton("+ Generate Invoice")
        add_btn.clicked.connect(lambda: self.show_message("Generate Invoice", "Feature coming soon"))
        export_btn = QPushButton("Export PDF")
        export_btn.clicked.connect(lambda: self.show_message("Export PDF", "Feature coming soon"))
        button_layout.addWidget(add_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Invoice #", "Repair ID", "Amount", "Status"])
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        
        tab.setLayout(layout)
        return tab
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About RepairQ",
                         "RepairQ v1.0\n\n"
                         "Professional Repair Shop Management Application\n\n"
                         "Built with Python and PyQt6\n\n"
                         "© 2026")
    
    def show_message(self, title: str, message: str):
        """Show information message"""
        QMessageBox.information(self, title, message)
