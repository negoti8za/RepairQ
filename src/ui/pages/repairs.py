"""
Repairs Page - Repair ticket management
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.repair_service import RepairService, ServiceCatalog
from src.services.customer_service import CustomerService
from src.services.database import Database


class RepairsPage(QWidget):
    """Repair tickets management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_tickets()
    
    def init_ui(self):
        """Initialize repairs page"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title and buttons
        title_layout = QHBoxLayout()
        title = QLabel("Repair Tickets")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        new_ticket_btn = QPushButton("New Ticket")
        new_ticket_btn.setMinimumWidth(100)
        new_ticket_btn.clicked.connect(self.create_ticket)
        title_layout.addWidget(new_ticket_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_tickets)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)
        
        # Tickets table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Ticket #", "Customer", "Status", "Priority", "Actions"])
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                gridline-color: {COLOR_BORDER};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {COLOR_SURFACE};
                padding: 5px;
                border: 1px solid {COLOR_BORDER};
            }}
        """)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_tickets(self):
        """Load all tickets into table"""
        tickets = RepairService.list_tickets()
        self.table.setRowCount(len(tickets))
        
        for row, ticket in enumerate(tickets):
            self.table.setItem(row, 0, QTableWidgetItem(str(ticket['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(ticket['ticket_number']))
            
            # Get customer name
            customer = CustomerService.get_customer(ticket['customer_id'])
            customer_name = customer['name'] if customer else f"Customer #{ticket['customer_id']}"
            self.table.setItem(row, 2, QTableWidgetItem(customer_name))
            
            self.table.setItem(row, 3, QTableWidgetItem(ticket['status']))
            self.table.setItem(row, 4, QTableWidgetItem(ticket['priority']))
            
            # Action button
            view_btn = QPushButton("View")
            view_btn.setMaximumWidth(60)
            view_btn.clicked.connect(lambda checked, t_id=ticket['id']: self.view_ticket(t_id))
            self.table.setCellWidget(row, 5, view_btn)
    
    def create_ticket(self):
        """Create new ticket dialog"""
        dialog = NewTicketDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_tickets()
            QMessageBox.information(self, "Success", "Ticket created successfully")
    
    def view_ticket(self, ticket_id: int):
        """View ticket details"""
        dialog = TicketDetailDialog(ticket_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_tickets()


class NewTicketDialog(QDialog):
    """Create new ticket dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Repair Ticket")
        self.setGeometry(300, 300, 600, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Customer selection
        QLabel("Customer:")
        layout.addWidget(QLabel("Customer:"))
        self.customer_combo = QComboBox()
        customers = CustomerService.list_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
        layout.addWidget(self.customer_combo)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description = QTextEdit()
        self.description.setMinimumHeight(100)
        layout.addWidget(self.description)
        
        # Priority
        layout.addWidget(QLabel("Priority:"))
        self.priority = QComboBox()
        self.priority.addItems(["LOW", "NORMAL", "HIGH", "URGENT"])
        layout.addWidget(self.priority)
        
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
    
    def accept(self):
        """Create ticket"""
        if not self.description.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Description required")
            return
        
        customer_id = self.customer_combo.currentData()
        RepairService.create_ticket(
            customer_id=customer_id,
            description=self.description.toPlainText(),
            priority=self.priority.currentText()
        )
        super().accept()


class TicketDetailDialog(QDialog):
    """View/edit ticket details"""
    
    def __init__(self, ticket_id: int, parent):
        super().__init__(parent)
        self.ticket_id = ticket_id
        self.ticket = RepairService.get_ticket(ticket_id)
        self.setWindowTitle(f"Ticket {self.ticket['ticket_number']}")
        self.setGeometry(300, 200, 800, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Ticket info
        info_text = f"""
        Ticket: {self.ticket['ticket_number']}
        Status: {self.ticket['status']}
        Priority: {self.ticket['priority']}
        Description: {self.ticket['description']}
        Created: {self.ticket['created_at']}
        """
        info_label = QLabel(info_text)
        info_label.setStyleSheet("background-color: #F3F3F3; padding: 10px; border-radius: 4px;")
        layout.addWidget(info_label)
        
        # Status dropdown
        layout.addWidget(QLabel("Update Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["PENDING", "IN_PROGRESS", "COMPLETED", "CANCELLED"])
        self.status_combo.setCurrentText(self.ticket['status'])
        layout.addWidget(self.status_combo)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_changes(self):
        """Save changes"""
        new_status = self.status_combo.currentText()
        RepairService.update_ticket(self.ticket_id, status=new_status)
        QMessageBox.information(self, "Success", "Ticket updated")
        self.accept()
