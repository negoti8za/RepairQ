"""
Invoices Page - Invoice management and billing
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.invoice_service import InvoiceService
from src.services.repair_service import RepairService


class InvoicesPage(QWidget):
    """Invoice management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_invoices()
    
    def init_ui(self):
        """Initialize invoices page"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title and buttons
        title_layout = QHBoxLayout()
        title = QLabel("Invoices")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        new_btn = QPushButton("New Invoice")
        new_btn.setMinimumWidth(100)
        new_btn.clicked.connect(self.create_invoice)
        title_layout.addWidget(new_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_invoices)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)
        
        # Invoices table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Invoice #", "Customer", "Amount", "Status", "Actions"])
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
    
    def load_invoices(self):
        """Load invoices into table"""
        invoices = InvoiceService.list_invoices()
        self.table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(str(invoice['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(invoice['invoice_number']))
            
            # Get customer name
            from src.services.customer_service import CustomerService
            customer = CustomerService.get_customer(invoice['customer_id'])
            customer_name = customer['name'] if customer else "Unknown"
            self.table.setItem(row, 2, QTableWidgetItem(customer_name))
            
            amount = f"${invoice['total_amount']:.2f}"
            self.table.setItem(row, 3, QTableWidgetItem(amount))
            
            status_item = QTableWidgetItem(invoice['status'])
            self.table.setItem(row, 4, status_item)
            
            btn_layout = QHBoxLayout()
            view_btn = QPushButton("View")
            view_btn.setMaximumWidth(50)
            view_btn.clicked.connect(lambda checked, iid=invoice['id']: self.view_invoice(iid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, iid=invoice['id']: self.delete_invoice(iid))
            
            container = QWidget()
            layout_h = QHBoxLayout()
            layout_h.addWidget(view_btn)
            layout_h.addWidget(delete_btn)
            container.setLayout(layout_h)
            self.table.setCellWidget(row, 5, container)
    
    def create_invoice(self):
        """Create new invoice"""
        dialog = NewInvoiceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ticket_id, subtotal, tax = dialog.get_data()
            ticket = RepairService.get_ticket(ticket_id)
            InvoiceService.create_invoice(ticket_id, ticket['customer_id'], subtotal, tax)
            self.load_invoices()
            QMessageBox.information(self, "Success", "Invoice created")
    
    def view_invoice(self, invoice_id: int):
        """View invoice"""
        invoice = InvoiceService.get_invoice(invoice_id)
        QMessageBox.information(self, f"Invoice {invoice['invoice_number']}",
            f"Status: {invoice['status']}\n"
            f"Amount: ${invoice['total_amount']:.2f}\n"
            f"Created: {invoice['created_at']}")
    
    def delete_invoice(self, invoice_id: int):
        """Delete invoice"""
        reply = QMessageBox.question(self, "Confirm", "Delete invoice?")
        if reply == QMessageBox.StandardButton.Yes:
            InvoiceService.delete_invoice(invoice_id)
            self.load_invoices()


class NewInvoiceDialog(QDialog):
    """Create invoice dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Invoice")
        self.setGeometry(300, 300, 500, 300)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Select ticket
        layout.addWidget(QLabel("Select Repair Ticket:"))
        self.ticket_combo = QComboBox()
        tickets = RepairService.list_tickets()
        for ticket in tickets:
            self.ticket_combo.addItem(f"{ticket['ticket_number']}", ticket['id'])
        layout.addWidget(self.ticket_combo)
        
        # Subtotal
        layout.addWidget(QLabel("Subtotal:"))
        self.subtotal = QDoubleSpinBox()
        self.subtotal.setMinimum(0)
        self.subtotal.setMaximum(99999)
        layout.addWidget(self.subtotal)
        
        # Tax
        layout.addWidget(QLabel("Tax:"))
        self.tax = QDoubleSpinBox()
        self.tax.setMinimum(0)
        self.tax.setMaximum(99999)
        layout.addWidget(self.tax)
        
        layout.addStretch()
        
        # Buttons
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
        """Get form data"""
        return (
            self.ticket_combo.currentData(),
            self.subtotal.value(),
            self.tax.value()
        )
