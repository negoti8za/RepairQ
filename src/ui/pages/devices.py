"""
Devices Page - Device tracking and management
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.database import Database
from src.services.customer_service import CustomerService


class DevicesPage(QWidget):
    """Device tracking and management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_devices()
    
    def init_ui(self):
        """Initialize devices page"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title and buttons
        title_layout = QHBoxLayout()
        title = QLabel("Devices")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        new_btn = QPushButton("New Device")
        new_btn.setMinimumWidth(100)
        new_btn.clicked.connect(self.create_device)
        title_layout.addWidget(new_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_devices)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)
        
        # Devices table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Brand", "Model", "Serial", "Customer", "Actions"])
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                gridline-color: {COLOR_BORDER};
            }}
            QHeaderView::section {{
                background-color: {COLOR_SURFACE};
                padding: 5px;
                border: 1px solid {COLOR_BORDER};
            }}
        """)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_devices(self):
        """Load devices into table"""
        results = Database.execute_query('''
            SELECT d.*, dt.name as type_name, c.name as customer_name
            FROM devices d
            LEFT JOIN device_types dt ON d.device_type_id = dt.id
            LEFT JOIN customers c ON d.customer_id = c.id
            ORDER BY d.created_at DESC
        ''')
        
        self.table.setRowCount(len(results))
        
        for row, device in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(device['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(device['type_name'] or ""))
            self.table.setItem(row, 2, QTableWidgetItem(device['brand'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(device['model'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(device['serial_number'] or ""))
            self.table.setItem(row, 5, QTableWidgetItem(device['customer_name'] or ""))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, did=device['id']: self.delete_device(did))
            self.table.setCellWidget(row, 6, delete_btn)
    
    def create_device(self):
        """Create new device"""
        dialog = DeviceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            device_type_id, brand, model, serial, customer_id, description = dialog.get_data()
            
            Database.execute_update('''
                INSERT INTO devices (device_type_id, customer_id, brand, model, serial_number, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (device_type_id, customer_id, brand, model, serial, description))
            
            self.load_devices()
            QMessageBox.information(self, "Success", "Device created")
    
    def delete_device(self, device_id: int):
        """Delete device"""
        reply = QMessageBox.question(self, "Confirm", "Delete device?")
        if reply == QMessageBox.StandardButton.Yes:
            Database.execute_update("DELETE FROM devices WHERE id = ?", (device_id,))
            self.load_devices()


class DeviceDialog(QDialog):
    """Device create/edit dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Device")
        self.setGeometry(300, 300, 500, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Customer
        layout.addWidget(QLabel("Customer:"))
        self.customer_combo = QComboBox()
        customers = CustomerService.list_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
        layout.addWidget(self.customer_combo)
        
        # Device type
        layout.addWidget(QLabel("Device Type:"))
        self.type_combo = QComboBox()
        types = Database.execute_query("SELECT id, name FROM device_types ORDER BY name")
        for device_type in types:
            self.type_combo.addItem(device_type['name'], device_type['id'])
        if not types:
            self.type_combo.addItem("Laptop", 1)
            self.type_combo.addItem("Desktop", 2)
            self.type_combo.addItem("Printer", 3)
        layout.addWidget(self.type_combo)
        
        # Brand
        layout.addWidget(QLabel("Brand:"))
        self.brand = QLineEdit()
        layout.addWidget(self.brand)
        
        # Model
        layout.addWidget(QLabel("Model:"))
        self.model = QLineEdit()
        layout.addWidget(self.model)
        
        # Serial
        layout.addWidget(QLabel("Serial Number:"))
        self.serial = QLineEdit()
        layout.addWidget(self.serial)
        
        layout.addStretch()
        
        # Buttons
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
        """Get form data"""
        return (
            self.type_combo.currentData(),
            self.brand.text(),
            self.model.text(),
            self.serial.text(),
            self.customer_combo.currentData(),
            ""
        )
