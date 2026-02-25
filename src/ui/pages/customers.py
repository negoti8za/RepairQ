"""
Customers Page - Customer management
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.customer_service import CustomerService


def make_table_read_only(table: QTableWidget) -> None:
    """Make a table read-only (cannot edit cells by clicking)"""
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


class CustomersPage(QWidget):
    """Customer management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_customers()
    
    def init_ui(self):
        """Initialize customers page"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title and buttons
        title_layout = QHBoxLayout()
        title = QLabel("Customers")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        new_btn = QPushButton("New Customer")
        new_btn.setMinimumWidth(100)
        new_btn.clicked.connect(self.create_customer)
        title_layout.addWidget(new_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_customers)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)
        
        # Customers table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "City", "Actions"])
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
        # Make columns stretch equally
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(6):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        # Make table read-only
        make_table_read_only(self.table)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_customers(self):
        """Load customers into table"""
        customers = CustomerService.list_customers()
        self.table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(customer['name']))
            self.table.setItem(row, 2, QTableWidgetItem(customer['phone'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(customer['email'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(customer['city'] or ""))
            
            # Actions cell
            btn_container = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(50)
            edit_btn.setMaximumHeight(28)
            edit_btn.clicked.connect(lambda checked, cid=customer['id']: self.edit_customer(cid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.setMaximumHeight(28)
            delete_btn.clicked.connect(lambda checked, cid=customer['id']: self.delete_customer(cid))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
            btn_container.setLayout(btn_layout)
            self.table.setCellWidget(row, 5, btn_container)
    
    def create_customer(self):
        """Create new customer"""
        dialog = CustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, phone, email, address, city, state, zip_code, notes = dialog.get_data()
            CustomerService.create_customer(name, phone, email, address, city, state, zip_code, notes)
            self.load_customers()
            QMessageBox.information(self, "Success", "Customer created")
    
    def edit_customer(self, customer_id: int):
        """Edit customer"""
        customer = CustomerService.get_customer(customer_id)
        dialog = CustomerDialog(self, customer)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, phone, email, address, city, state, zip_code, notes = dialog.get_data()
            CustomerService.update_customer(customer_id, name=name, phone=phone, email=email,
                                          address=address, city=city, state=state, 
                                          zip_code=zip_code, notes=notes)
            self.load_customers()
            QMessageBox.information(self, "Success", "Customer updated")
    
    def delete_customer(self, customer_id: int):
        """Delete customer"""
        reply = QMessageBox.question(self, "Confirm", "Delete customer?")
        if reply == QMessageBox.StandardButton.Yes:
            CustomerService.delete_customer(customer_id)
            self.load_customers()
            QMessageBox.information(self, "Success", "Customer deleted")


class CustomerDialog(QDialog):
    """Customer edit/create dialog"""
    
    def __init__(self, parent, customer=None):
        super().__init__(parent)
        self.customer = customer
        self.setWindowTitle("Customer" if not customer else f"Edit {customer['name']}")
        self.setGeometry(300, 300, 500, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        fields = [
            ("Name", "name"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
            ("City", "city"),
            ("State", "state"),
            ("Zip Code", "zip_code"),
        ]
        
        self.inputs = {}
        for label, key in fields:
            layout.addWidget(QLabel(label))
            input_field = QLineEdit()
            if self.customer:
                input_field.setText(str(self.customer.get(key, "")))
            self.inputs[key] = input_field
            layout.addWidget(input_field)
        
        layout.addWidget(QLabel("Notes"))
        self.notes_input = QTextEdit()
        if self.customer:
            self.notes_input.setText(self.customer.get('notes', ""))
        self.notes_input.setMinimumHeight(80)
        layout.addWidget(self.notes_input)
        
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
            self.inputs['name'].text(),
            self.inputs['phone'].text(),
            self.inputs['email'].text(),
            self.inputs['address'].text(),
            self.inputs['city'].text(),
            self.inputs['state'].text(),
            self.inputs['zip_code'].text(),
            self.notes_input.toPlainText(),
        )
