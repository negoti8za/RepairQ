"""
Admin Panel - System setup and administration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox,
    QMessageBox, QSpinBox, QDoubleSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.database import Database
from src.services.auth import AuthService


class AdminPanel(QWidget):
    """Admin control panel"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize admin panel"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Admin Panel")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabbed interface
        self.tabs = QTabWidget()
        self.tabs.addTab(UsersTab(), "Users")
        self.tabs.addTab(ServiceCatalogTab(), "Repair Services")
        self.tabs.addTab(SettingsTab(), "Settings")
        self.tabs.addTab(DeviceTypesTab(), "Device Types")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)


class UsersTab(QWidget):
    """User management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize users tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        new_btn = QPushButton("Add User")
        new_btn.clicked.connect(self.create_user)
        button_layout.addWidget(new_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Users table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Name", "Email", "Role", "Actions"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_users(self):
        """Load users"""
        results = Database.execute_query("SELECT id, username, first_name, email, role FROM users ORDER BY username")
        self.table.setRowCount(len(results))
        
        for row, user in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.table.setItem(row, 2, QTableWidgetItem(user['first_name'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(user['email'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(user['role']))
            
            btn_layout = QHBoxLayout()
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(50)
            edit_btn.clicked.connect(lambda checked, uid=user['id']: self.edit_user(uid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, uid=user['id']: self.delete_user(uid))
            
            container = QWidget()
            layout_h = QHBoxLayout()
            layout_h.addWidget(edit_btn)
            layout_h.addWidget(delete_btn)
            container.setLayout(layout_h)
            self.table.setCellWidget(row, 5, container)
    
    def create_user(self):
        """Create user"""
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, email, first_name, role = dialog.get_data()
            password = "changeme"  # Default password
            from src.services.database import Database as DB
            password_hash = DB._hash_password(password)
            
            Database.execute_update('''
                INSERT INTO users (username, password_hash, email, first_name, role, password_changed)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (username, password_hash, email, first_name, role))
            
            self.load_users()
            QMessageBox.information(self, "Success", f"User created. Default password: {password}")
    
    def edit_user(self, user_id: int):
        """Edit user"""
        QMessageBox.information(self, "Edit", "Edit user functionality - Coming soon")
    
    def delete_user(self, user_id: int):
        """Delete user"""
        reply = QMessageBox.question(self, "Confirm", "Delete user?")
        if reply == QMessageBox.StandardButton.Yes:
            Database.execute_update("DELETE FROM users WHERE id = ?", (user_id,))
            self.load_users()


class UserDialog(QDialog):
    """Create user dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add User")
        self.setGeometry(300, 300, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)
        
        layout.addWidget(QLabel("First Name:"))
        self.first_name = QLineEdit()
        layout.addWidget(self.first_name)
        
        layout.addWidget(QLabel("Role:"))
        self.role = QComboBox()
        self.role.addItems(["ADMIN", "STAFF", "TECHNICIAN"])
        layout.addWidget(self.role)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Create")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Get data"""
        return self.username.text(), self.email.text(), self.first_name.text(), self.role.currentText()


class ServiceCatalogTab(QWidget):
    """Repair services management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_services()
    
    def init_ui(self):
        """Initialize services tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        button_layout = QHBoxLayout()
        new_btn = QPushButton("Add Service")
        new_btn.clicked.connect(self.create_service)
        button_layout.addWidget(new_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Actions"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_services(self):
        """Load services"""
        from src.services.repair_service import ServiceCatalog
        services = ServiceCatalog.list_services()
        self.table.setRowCount(len(services))
        
        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(service['name']))
            self.table.setItem(row, 2, QTableWidgetItem(service['category'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(f"${service['base_price']:.2f}"))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, sid=service['id']: self.delete_service(sid))
            self.table.setCellWidget(row, 4, delete_btn)
    
    def create_service(self):
        """Create service"""
        dialog = ServiceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, category, price = dialog.get_data()
            from src.services.repair_service import ServiceCatalog
            ServiceCatalog.create_service(name, category, price)
            self.load_services()
            QMessageBox.information(self, "Success", "Service created")
    
    def delete_service(self, service_id: int):
        """Delete service"""
        reply = QMessageBox.question(self, "Confirm", "Delete service?")
        if reply == QMessageBox.StandardButton.Yes:
            from src.services.repair_service import ServiceCatalog
            ServiceCatalog.delete_service(service_id)
            self.load_services()


class ServiceDialog(QDialog):
    """Create service dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add Service")
        self.setGeometry(300, 300, 400, 250)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Service Name:"))
        self.name = QLineEdit()
        layout.addWidget(self.name)
        
        layout.addWidget(QLabel("Category:"))
        self.category = QLineEdit()
        layout.addWidget(self.category)
        
        layout.addWidget(QLabel("Base Price:"))
        self.price = QDoubleSpinBox()
        self.price.setMinimum(0)
        self.price.setMaximum(99999)
        layout.addWidget(self.price)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Add")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Get data"""
        return self.name.text(), self.category.text(), self.price.value()


class SettingsTab(QWidget):
    """Application settings"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize settings tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.settings_dict = {}
        
        for key in SETTINGS.keys():
            layout.addWidget(QLabel(f"{key.replace('_', ' ').title()}:"))
            input_field = QLineEdit()
            self.settings_dict[key] = input_field
            layout.addWidget(input_field)
        
        layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load settings from database"""
        for key in SETTINGS.keys():
            result = Database.execute_query("SELECT value FROM settings WHERE key = ?", (key,))
            if result:
                self.settings_dict[key].setText(result[0]['value'])
    
    def save_settings(self):
        """Save settings"""
        for key, input_field in self.settings_dict.items():
            value = input_field.text()
            Database.execute_update(
                "UPDATE settings SET value = ? WHERE key = ?",
                (value, key)
            )
        QMessageBox.information(self, "Success", "Settings saved")


class DeviceTypesTab(QWidget):
    """Device types management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_types()
    
    def init_ui(self):
        """Initialize device types tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        button_layout = QHBoxLayout()
        new_btn = QPushButton("Add Type")
        new_btn.clicked.connect(self.create_type)
        button_layout.addWidget(new_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_types(self):
        """Load device types"""
        results = Database.execute_query("SELECT id, name FROM device_types ORDER BY name")
        self.table.setRowCount(len(results))
        
        for row, dtype in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(dtype['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(dtype['name']))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, tid=dtype['id']: self.delete_type(tid))
            self.table.setCellWidget(row, 2, delete_btn)
    
    def create_type(self):
        """Create device type"""
        name, ok = self.get_input("Device Type Name:")
        if ok and name:
            Database.execute_update(
                "INSERT INTO device_types (name) VALUES (?)",
                (name,)
            )
            self.load_types()
    
    def delete_type(self, type_id: int):
        """Delete device type"""
        reply = QMessageBox.question(self, "Confirm", "Delete device type?")
        if reply == QMessageBox.StandardButton.Yes:
            Database.execute_update("DELETE FROM device_types WHERE id = ?", (type_id,))
            self.load_types()
    
    def get_input(self, prompt: str) -> tuple:
        """Get input from user"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Input")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(prompt))
        input_field = QLineEdit()
        layout.addWidget(input_field)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        ok = dialog.exec() == QDialog.DialogCode.Accepted
        return input_field.text(), ok
