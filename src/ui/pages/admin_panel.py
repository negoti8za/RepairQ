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
from src.services.repair_service import RepairService
from src.services.invoice_service import InvoiceService
from src.services.customer_service import CustomerService
from src.utils.logger import AppLogger


def make_table_read_only(table: QTableWidget) -> None:
    """Make a table read-only (cannot edit cells by clicking)"""
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


class AdminPanel(QWidget):
    """Admin control panel"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            AppLogger.info("AdminPanel initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing AdminPanel: {e}")
            raise
    
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
        
        # Add tabs with error handling
        tabs_config = [
            ("Users", UsersTab),
            ("Repair Services", ServiceCatalogTab),
            ("Service Categories", ServiceCategoriesTab),
            ("Settings", SettingsTab),
            ("Device Types", DeviceTypesTab),
            ("Invoice Tracking", InvoiceTrackingTab),
            ("Invoice Setup", InvoiceCustomizationTab),
        ]
        
        for tab_name, tab_class in tabs_config:
            try:
                tab = tab_class()
                self.tabs.addTab(tab, tab_name)
                AppLogger.info(f"Loaded admin tab: {tab_name}")
            except Exception as e:
                AppLogger.error(f"Error loading admin tab '{tab_name}': {e}")
                import traceback
                traceback.print_exc()
                error_widget = QWidget()
                error_layout = QVBoxLayout()
                error_layout.addWidget(QLabel(f"Error loading {tab_name}\n{str(e)[:100]}"))
                error_widget.setLayout(error_layout)
                self.tabs.addTab(error_widget, f"{tab_name} (Error)")
        
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
        # Make columns stretch equally
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(6):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        # Make table read-only
        make_table_read_only(self.table)
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
            
            container = QWidget()
            layout_h = QHBoxLayout()
            layout_h.setContentsMargins(2, 2, 2, 2)
            layout_h.setSpacing(3)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(60)
            edit_btn.clicked.connect(lambda checked, uid=user['id']: self.edit_user(uid))
            layout_h.addWidget(edit_btn)
            
            reset_btn = QPushButton("Reset Pwd")
            reset_btn.setMaximumWidth(80)
            reset_btn.clicked.connect(lambda checked, uid=user['id']: self.reset_password(uid))
            layout_h.addWidget(reset_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(65)
            delete_btn.clicked.connect(lambda checked, uid=user['id']: self.delete_user(uid))
            layout_h.addWidget(delete_btn)
            
            layout_h.addStretch()
            container.setLayout(layout_h)
            self.table.setCellWidget(row, 5, container)
    
    def create_user(self):
        """Create user"""
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, email, first_name, role, password = dialog.get_data()
            from src.services.database import Database as DB
            password_hash = DB._hash_password(password)
            
            Database.execute_update('''
                INSERT INTO users (username, password_hash, email, first_name, role, password_changed)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (username, password_hash, email, first_name, role))
            
            self.load_users()
            QMessageBox.information(self, "Success", f"User created with password set.")
    
    def edit_user(self, user_id: int):
        """Edit user"""
        result = Database.execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
        if not result:
            return
        
        user = dict(result[0])
        dialog = EditUserDialog(user, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            email, first_name, role = dialog.get_data()
            Database.execute_update('''
                UPDATE users SET email = ?, first_name = ?, role = ? WHERE id = ?
            ''', (email, first_name, role, user_id))
            self.load_users()
            QMessageBox.information(self, "Success", "User updated")
    
    def delete_user(self, user_id: int):
        """Delete user"""
        reply = QMessageBox.question(self, "Confirm", "Delete user?")
        if reply == QMessageBox.StandardButton.Yes:
            Database.execute_update("DELETE FROM users WHERE id = ?", (user_id,))
            self.load_users()
    
    def reset_password(self, user_id: int):
        """Reset user password"""
        result = Database.execute_query("SELECT username FROM users WHERE id = ?", (user_id,))
        if not result:
            return
        
        username = result[0]['username']
        new_password, ok = self._prompt_new_password()
        if ok and new_password:
            from src.services.database import Database as DB
            password_hash = DB._hash_password(new_password)
            Database.execute_update(
                "UPDATE users SET password_hash = ?, password_changed = 0 WHERE id = ?",
                (password_hash, user_id)
            )
            QMessageBox.information(self, "Success", f"Password for {username} has been reset")
            self.load_users()
    
    def _prompt_new_password(self):
        """Prompt for new password"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Reset Password")
        dialog.setGeometry(400, 400, 300, 150)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("New Password:"))
        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_field)
        
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
        return password_field.text(), ok
    
    def reset_password(self, user_id: int):
        """Reset user password"""
        result = Database.execute_query("SELECT username FROM users WHERE id = ?", (user_id,))
        if not result:
            return
        
        username = result[0]['username']
        new_password, ok = self._prompt_new_password()
        if ok and new_password:
            from src.services.database import Database as DB
            password_hash = DB._hash_password(new_password)
            Database.execute_update(
                "UPDATE users SET password_hash = ?, password_changed = 0 WHERE id = ?",
                (password_hash, user_id)
            )
            QMessageBox.information(self, "Success", f"Password for {username} has been reset")
            self.load_users()
    
    def _prompt_new_password(self):
        """Prompt for new password"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Reset Password")
        dialog.setGeometry(400, 400, 300, 150)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("New Password:"))
        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_field)
        
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
        return password_field.text(), ok


class UserDialog(QDialog):
    """Create user dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add User")
        self.setGeometry(300, 300, 400, 400)
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
        
        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)
        
        layout.addWidget(QLabel("Confirm Password:"))
        self.password_confirm = QLineEdit()
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_confirm)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Create")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        """Validate and accept"""
        if not self.password.text() or not self.password_confirm.text():
            QMessageBox.warning(self, "Error", "Password is required")
            return
        if self.password.text() != self.password_confirm.text():
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        self.accept()
    
    def get_data(self):
        """Get data"""
        return (self.username.text(), self.email.text(), self.first_name.text(), 
                self.role.currentText(), self.password.text())


class EditUserDialog(QDialog):
    """Edit user dialog"""
    
    def __init__(self, user, parent):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle(f"Edit {user['username']}")
        self.setGeometry(300, 300, 400, 250)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        self.email.setText(self.user.get('email') or "")
        layout.addWidget(self.email)
        
        layout.addWidget(QLabel("First Name:"))
        self.first_name = QLineEdit()
        self.first_name.setText(self.user.get('first_name') or "")
        layout.addWidget(self.first_name)
        
        layout.addWidget(QLabel("Role:"))
        self.role = QComboBox()
        self.role.addItems(["ADMIN", "STAFF", "TECHNICIAN"])
        self.role.setCurrentText(self.user.get('role', 'STAFF'))
        layout.addWidget(self.role)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
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
        return self.email.text(), self.first_name.text(), self.role.currentText()


class ServiceCatalogTab(QWidget):
    """Repair services management"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.load_services()
            AppLogger.info("ServiceCatalogTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing ServiceCatalogTab: {e}")
            raise
    
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
        # Make columns stretch equally
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        # Make table read-only
        make_table_read_only(self.table)
        for i in range(5):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_services(self):
        """Load services"""
        from src.services.repair_service import ServiceCatalog
        services = ServiceCatalog.list_services()
        self.table.setRowCount(len(services))
        
        # Get currency symbol
        currency_result = Database.execute_query("SELECT currency FROM invoice_customization LIMIT 1")
        currency = currency_result[0]['currency'] if currency_result else 'USD'
        symbol = self._get_currency_symbol(currency)
        
        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(service['name']))
            self.table.setItem(row, 2, QTableWidgetItem(service['category'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(f"{symbol}{service['base_price']:.2f}"))
            
            # Actions
            btn_container = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(50)
            edit_btn.clicked.connect(lambda checked, sid=service['id']: self.edit_service(sid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, sid=service['id']: self.delete_service(sid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
            btn_container.setLayout(btn_layout)
            self.table.setCellWidget(row, 4, btn_container)
    
    def create_service(self):
        """Create service"""
        dialog = ServiceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, category, price = dialog.get_data()
            category_id = dialog.category.currentData()
            Database.execute_update(
                "INSERT INTO repair_services (name, category, category_id, base_price) VALUES (?, ?, ?, ?)",
                (name, category, category_id, price)
            )
            self.load_services()
            QMessageBox.information(self, "Success", "Service created")
    
    def edit_service(self, service_id: int):
        """Edit service"""
        from src.services.repair_service import ServiceCatalog
        service = ServiceCatalog.get_service(service_id)
        if not service:
            return
        
        dialog = ServiceDialog(self, service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, category, price = dialog.get_data()
            category_id = dialog.category.currentData()
            Database.execute_update(
                "UPDATE repair_services SET name = ?, category = ?, category_id = ?, base_price = ? WHERE id = ?",
                (name, category, category_id, price, service_id)
            )
            self.load_services()
            QMessageBox.information(self, "Success", "Service updated")
    
    def delete_service(self, service_id: int):
        """Delete service"""
        reply = QMessageBox.question(self, "Confirm", "Delete service?")
        if reply == QMessageBox.StandardButton.Yes:
            from src.services.repair_service import ServiceCatalog
            ServiceCatalog.delete_service(service_id)
            self.load_services()
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol for currency code"""
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CAD': '$',
            'AUD': '$',
            'CHF': 'CHF',
            'CNY': '¥',
            'INR': '₹',
            'MXN': '$',
            'AED': 'د.إ',
            'SGD': '$',
            'HKD': '$',
            'NZD': '$',
        }
        return symbols.get(currency_code, currency_code + ' ')


class ServiceDialog(QDialog):
    """Create/edit service dialog"""
    
    def __init__(self, parent, service=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Edit Service" if service else "Add Service")
        self.setGeometry(300, 300, 400, 250)
        self.init_ui()
        if service:
            self.name.setText(service.get('name', ''))
            # Set category combo to match category_id or name
            category_id = service.get('category_id')
            if category_id:
                for i in range(self.category.count()):
                    if self.category.itemData(i) == category_id:
                        self.category.setCurrentIndex(i)
                        break
            self.price.setValue(float(service.get('base_price', 0)))
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Service Name:"))
        self.name = QLineEdit()
        layout.addWidget(self.name)
        
        layout.addWidget(QLabel("Category:"))
        self.category = QComboBox()
        self.category.addItem("-- Select Category --", None)
        # Load categories from database
        categories = Database.execute_query("SELECT id, name FROM service_categories ORDER BY name")
        for cat in categories:
            self.category.addItem(cat['name'], cat['id'])
        layout.addWidget(self.category)
        
        layout.addWidget(QLabel("Base Price:"))
        self.price = QDoubleSpinBox()
        self.price.setMinimum(0)
        self.price.setMaximum(99999)
        layout.addWidget(self.price)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save" if self.service else "Add")
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
        # Return category name for backward compatibility, along with category_id
        category_id = self.category.currentData()
        category_name = self.category.currentText() if category_id else ""
        return self.name.text(), category_name, self.price.value()


class ServiceCategoriesTab(QWidget):
    """Service categories management"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.load_categories()
            AppLogger.info("ServiceCategoriesTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing ServiceCategoriesTab: {e}")
            raise
    
    def init_ui(self):
        """Initialize categories tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        button_layout = QHBoxLayout()
        new_btn = QPushButton("Add Category")
        new_btn.clicked.connect(self.create_category)
        button_layout.addWidget(new_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Actions"])
        make_table_read_only(self.table)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(2):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_categories(self):
        """Load service categories"""
        results = Database.execute_query("SELECT id, name FROM service_categories ORDER BY name")
        self.table.setRowCount(len(results))
        
        for row, category in enumerate(results):
            self.table.setRowHeight(row, 35)
            self.table.setItem(row, 0, QTableWidgetItem(category['name']))
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setMinimumWidth(55)
            delete_btn.setMinimumHeight(32)
            delete_btn.setMaximumWidth(70)
            delete_btn.setStyleSheet(f"background-color: {COLOR_DANGER}; color: white; border: none; padding: 4px 8px; font-weight: bold;")
            delete_btn.clicked.connect(lambda checked, cid=category['id']: self.delete_category(cid))
            self.table.setCellWidget(row, 1, delete_btn)
    
    def create_category(self):
        """Create category"""
        name, ok = self.get_input("Category Name:")
        if ok and name:
            Database.execute_update(
                "INSERT INTO service_categories (name) VALUES (?)",
                (name,)
            )
            self.load_categories()
            QMessageBox.information(self, "Success", "Category created")
    
    def delete_category(self, category_id: int):
        """Delete category"""
        # Check if category is in use
        in_use = Database.execute_query(
            "SELECT COUNT(*) as count FROM repair_services WHERE category_id = ?",
            (category_id,)
        )
        if in_use and in_use[0]['count'] > 0:
            QMessageBox.warning(self, "Error", f"Cannot delete: {in_use[0]['count']} service(s) use this category")
            return
        
        reply = QMessageBox.question(self, "Confirm", "Delete category?")
        if reply == QMessageBox.StandardButton.Yes:
            Database.execute_update("DELETE FROM service_categories WHERE id = ?", (category_id,))
            self.load_categories()
    
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


class SettingsTab(QWidget):
    """Application settings"""
    
    def __init__(self):
        super().__init__()
        self.settings_dict = {}
        try:
            self.init_ui()
            self.load_settings()
            AppLogger.info("SettingsTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing SettingsTab: {e}")
            raise
    
    def init_ui(self):
        """Initialize settings tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Company settings
        self.settings_dict = {}
        for key in SETTINGS.keys():
            layout.addWidget(QLabel(f"{key.replace('_', ' ').title()}:"))
            input_field = QLineEdit()
            self.settings_dict[key] = input_field
            layout.addWidget(input_field)
        
        # Tax Rate
        layout.addWidget(QLabel("Tax Rate (%):"))
        self.tax_rate = QDoubleSpinBox()
        self.tax_rate.setMinimum(0)
        self.tax_rate.setMaximum(100)
        self.tax_rate.setValue(8)
        layout.addWidget(self.tax_rate)
        
        # Currency Dropdown
        layout.addWidget(QLabel("Currency:"))
        self.currency = QComboBox()
        from src.config import CURRENCIES
        self.currency.addItems(CURRENCIES)
        layout.addWidget(self.currency)
        
        # Logo Upload
        layout.addWidget(QLabel("Company Logo:"))
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel("No logo selected")
        logo_layout.addWidget(self.logo_label)
        logo_btn = QPushButton("Upload Logo")
        logo_btn.setMaximumWidth(120)
        logo_btn.clicked.connect(self.upload_logo)
        logo_layout.addWidget(logo_btn)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)
        
        layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load settings from database"""
        # Load company settings
        for key in SETTINGS.keys():
            result = Database.execute_query("SELECT value FROM settings WHERE key = ?", (key,))
            if result:
                self.settings_dict[key].setText(result[0]['value'])
        
        # Load tax and currency
        result = Database.execute_query("SELECT tax_rate, currency FROM invoice_customization LIMIT 1")
        if result:
            self.tax_rate.setValue(float(result[0]['tax_rate']))
            curr = result[0]['currency']
            idx = self.currency.findText(curr)
            if idx >= 0:
                self.currency.setCurrentIndex(idx)
    
    def upload_logo(self):
        """Upload company logo"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            # Store logo in invoice_customization table (company_logo BLOB column)
            try:
                with open(file_path, 'rb') as f:
                    logo_data = f.read()
                
                # Store in invoice_customization table
                Database.execute_update(
                    "UPDATE invoice_customization SET company_logo = ? WHERE id = (SELECT id FROM invoice_customization LIMIT 1)",
                    (logo_data,)
                )
                
                import os
                self.logo_label.setText(f"Logo uploaded: {os.path.basename(file_path)}")
                QMessageBox.information(self, "Success", "Logo uploaded and saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload logo: {str(e)}")
    
    def save_settings(self):
        """Save settings"""
        # Save company settings
        for key, input_field in self.settings_dict.items():
            value = input_field.text()
            Database.execute_update(
                "UPDATE settings SET value = ? WHERE key = ?",
                (value, key)
            )
        
        # Save tax rate and currency
        Database.execute_update(
            "UPDATE invoice_customization SET tax_rate = ?, currency = ? WHERE id = (SELECT id FROM invoice_customization LIMIT 1)",
            (self.tax_rate.value(), self.currency.currentText())
        )
        QMessageBox.information(self, "Success", "Settings saved")


class DeviceTypesTab(QWidget):
    """Device types management"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.load_types()
            AppLogger.info("DeviceTypesTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing DeviceTypesTab: {e}")
            raise
    
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
        # Make columns stretch equally
        # Make table read-only
        make_table_read_only(self.table)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(3):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
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
        # Check if device type is in use
        in_use = Database.execute_query(
            "SELECT COUNT(*) as count FROM devices WHERE device_type_id = ?",
            (type_id,)
        )
        if in_use and in_use[0]['count'] > 0:
            QMessageBox.warning(self, "Error", f"Cannot delete: {in_use[0]['count']} device(s) use this device type")
            return
        
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


class InvoiceCustomizationTab(QWidget):
    """Invoice customization settings"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.load_settings()
            AppLogger.info("InvoiceCustomizationTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing InvoiceCustomizationTab: {e}")
            raise
    
    def init_ui(self):
        """Initialize invoice customization tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Invoice header
        layout.addWidget(QLabel("Invoice Header:"))
        self.header = QTextEdit()
        self.header.setMinimumHeight(60)
        layout.addWidget(self.header)
        
        # Invoice footer
        layout.addWidget(QLabel("Invoice Footer:"))
        self.footer = QTextEdit()
        self.footer.setMinimumHeight(60)
        layout.addWidget(self.footer)
        
        # Invoice terms
        layout.addWidget(QLabel("Invoice Terms & Conditions:"))
        self.terms = QTextEdit()
        self.terms.setMinimumHeight(80)
        layout.addWidget(self.terms)
        
        layout.addStretch()
        
        # Info label
        info_label = QLabel("Note: Tax Rate and Currency are set in Settings tab")
        info_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(info_label)
        
        # Save button
        save_btn = QPushButton("Save Invoice Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load invoice settings from database"""
        result = Database.execute_query("SELECT * FROM invoice_customization LIMIT 1")
        if result:
            settings = dict(result[0])
            self.header.setPlainText(settings.get('invoice_header', ''))
            self.footer.setPlainText(settings.get('invoice_footer', ''))
            self.terms.setPlainText(settings.get('invoice_terms', ''))
        else:
            # Insert default
            Database.execute_update('''
                INSERT INTO invoice_customization 
                (tax_rate, currency, invoice_header, invoice_footer, invoice_terms)
                VALUES (?, ?, ?, ?, ?)
            ''', (8, 'USD', '', '', ''))
    
    def save_settings(self):
        """Save invoice settings"""
        Database.execute_update('''
            UPDATE invoice_customization
            SET invoice_header = ?, invoice_footer = ?, invoice_terms = ?
            WHERE id = (SELECT id FROM invoice_customization LIMIT 1)
        ''', (
            self.header.toPlainText(),
            self.footer.toPlainText(),
            self.terms.toPlainText()
        ))
        QMessageBox.information(self, "Success", "Invoice settings saved")


class InvoiceTrackingTab(QWidget):
    """Invoice tracking and management"""
    
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.load_invoices()
            AppLogger.info("InvoiceTrackingTab initialized successfully")
        except Exception as e:
            AppLogger.error(f"Error initializing InvoiceTrackingTab: {e}")
            raise
    
    def init_ui(self):
        """Initialize invoice tracking tab"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Filter by status with refresh button
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["ALL", "PENDING", "SENT", "PAID", "CANCELLED"])
        self.status_filter.currentTextChanged.connect(self.on_status_filter_changed)
        filter_layout.addWidget(self.status_filter)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(80)
        refresh_btn.clicked.connect(self.load_invoices)
        filter_layout.addWidget(refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Invoices table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Invoice #", "Customer", "Ticket #", "Amount", "Status", "Outstanding", "Actions"])
        make_table_read_only(self.table)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        for i in range(7):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def on_status_filter_changed(self):
        """Reload when status filter changes"""
        self.load_invoices()
    
    def load_invoices(self):
        """Load invoices filtered by status"""
        status_filter = self.status_filter.currentText()
        
        if status_filter == "ALL":
            invoices = InvoiceService.list_invoices()
        else:
            invoices = InvoiceService.list_invoices(status_filter)
        
        self.table.setRowCount(len(invoices))
        
        # Get currency
        try:
            currency_result = Database.execute_query("SELECT currency FROM invoice_customization LIMIT 1")
            if currency_result:
                currency_row = dict(currency_result[0]) if hasattr(currency_result[0], 'keys') else currency_result[0]
                currency = currency_row.get('currency', 'USD')
            else:
                currency = 'USD'
        except Exception:
            currency = 'USD'
        symbol = self._get_currency_symbol(currency)
        
        for row, invoice in enumerate(invoices):
            self.table.setRowHeight(row, 35)
            invoice_dict = dict(invoice) if hasattr(invoice, 'keys') else invoice
            
            self.table.setItem(row, 0, QTableWidgetItem(invoice_dict.get('invoice_number', '')))
            
            # Get customer name
            customer = CustomerService.get_customer(invoice_dict.get('customer_id'))
            customer_name = customer['name'] if customer else f"Cust #{invoice_dict.get('customer_id')}"
            self.table.setItem(row, 1, QTableWidgetItem(customer_name))
            
            # Get ticket number
            ticket = RepairService.get_ticket(invoice_dict.get('repair_ticket_id'))
            ticket_number = ticket['ticket_number'] if ticket else f"#{invoice_dict.get('repair_ticket_id')}"
            self.table.setItem(row, 2, QTableWidgetItem(ticket_number))
            
            amount = f"{symbol}{invoice_dict.get('total_amount', 0):.2f}"
            self.table.setItem(row, 3, QTableWidgetItem(amount))
            
            status = invoice_dict.get('status', 'PENDING')
            self.table.setItem(row, 4, QTableWidgetItem(status))
            
            # Calculate outstanding amount (total - if paid)
            outstanding = 0 if status == 'PAID' else invoice_dict.get('total_amount', 0)
            outstanding_text = f"{symbol}{outstanding:.2f}" if outstanding > 0 else "Paid"
            self.table.setItem(row, 5, QTableWidgetItem(outstanding_text))
            
            # Actions
            container = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            view_btn = QPushButton("View")
            view_btn.setMaximumWidth(55)
            view_btn.clicked.connect(lambda checked, iid=invoice_dict.get('id'): self.view_invoice(iid))
            btn_layout.addWidget(view_btn)
            
            btn_layout.addStretch()
            container.setLayout(btn_layout)
            self.table.setCellWidget(row, 6, container)
    
    def view_invoice(self, invoice_id: int):
        """View and edit invoice"""
        from src.ui.pages.invoices import InvoiceDetailDialog
        dialog = InvoiceDetailDialog(invoice_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_invoices()
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol"""
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CAD': '$', 'AUD': '$',
            'CHF': 'CHF', 'CNY': '¥', 'INR': '₹', 'MXN': '$', 'AED': 'د.إ', 'SGD': '$',
            'HKD': '$', 'NZD': '$',
        }
        return symbols.get(currency_code, currency_code + ' ')



