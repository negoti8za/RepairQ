"""
Repairs Page - Repair ticket management
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QMessageBox, QTabWidget, QCheckBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.repair_service import RepairService, ServiceCatalog
from src.services.customer_service import CustomerService
from src.services.database import Database
from src.services.auth import AuthService
from src.utils.logger import AppLogger


def make_table_read_only(table: QTableWidget) -> None:
    """Make a table read-only (cannot edit cells by clicking)"""
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


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
        # Make columns stretch equally
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(6):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        # Make table read-only and ensure rows are tall enough for action buttons
        make_table_read_only(self.table)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.verticalHeader().setMinimumSectionSize(38)
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
            
            # Action buttons
            container = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(3)
            
            view_btn = QPushButton("View")
            view_btn.setMaximumWidth(60)
            view_btn.clicked.connect(lambda checked, t_id=ticket['id']: self.view_ticket(t_id))
            btn_layout.addWidget(view_btn)
            
            # Show delete button only for admin users
            auth_user = AuthService.get_current_user()
            if auth_user and auth_user['role'] == 'ADMIN':
                delete_btn = QPushButton("Delete")
                delete_btn.setMaximumWidth(65)
                delete_btn.setStyleSheet(f"background-color: {COLOR_DANGER}; color: white; border: none; padding: 3px; font-weight: bold; font-size: 11px;")
                delete_btn.clicked.connect(lambda checked, t_id=ticket['id']: self.delete_ticket(t_id))
                btn_layout.addWidget(delete_btn)
            
            btn_layout.addStretch()
            container.setLayout(btn_layout)
            self.table.setCellWidget(row, 5, container)
    
    def create_ticket(self):
        """Create new ticket dialog"""
        dialog = NewTicketDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_tickets()
            QMessageBox.information(self, "Success", "Ticket created successfully")
    
    def view_ticket(self, ticket_id: int):
        """View ticket details"""
        try:
            dialog = TicketDetailDialog(ticket_id, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_tickets()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open ticket: {str(e)}")
            print(f"Ticket view error: {e}")
            import traceback
            traceback.print_exc()
    
    def delete_ticket(self, ticket_id: int):
        """Delete a repair ticket (admin only)"""
        reply = QMessageBox.question(self, "Confirm Delete", 
            "Are you sure you want to delete this ticket?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                Database.execute_update("DELETE FROM repair_items WHERE repair_ticket_id = ?", (ticket_id,))
                Database.execute_update("DELETE FROM ticket_notes WHERE repair_ticket_id = ?", (ticket_id,))
                Database.execute_update("DELETE FROM invoices WHERE repair_ticket_id = ?", (ticket_id,))
                Database.execute_update("DELETE FROM repair_tickets WHERE id = ?", (ticket_id,))
                self.load_tickets()
                QMessageBox.information(self, "Success", "Ticket deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete ticket: {str(e)}")


class NewTicketDialog(QDialog):
    """Create new ticket dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Repair Ticket")
        self.setGeometry(300, 300, 700, 700)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Customer selection
        layout.addWidget(QLabel("Customer:"))
        self.customer_combo = QComboBox()
        customers = CustomerService.list_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
        self.customer_combo.currentIndexChanged.connect(self.on_customer_changed)
        layout.addWidget(self.customer_combo)
        
        # Device selection
        layout.addWidget(QLabel("Select Device:"))
        self.device_combo = QComboBox()
        self.device_combo.currentIndexChanged.connect(self.on_device_changed)
        layout.addWidget(self.device_combo)
        
        # Load devices for first customer if exists
        if self.customer_combo.count() > 0:
            self.on_customer_changed()
        
        # Device type (read-only, from selected device)
        layout.addWidget(QLabel("Device Type:"))
        self.device_type_label = QLabel()
        self.device_type_label.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #f9f9f9;")
        layout.addWidget(self.device_type_label)
        
        # Device brand and model (read-only, from selected device)
        brand_model_layout = QHBoxLayout()
        brand_model_layout.addWidget(QLabel("Brand:"))
        self.device_brand = QLabel()
        self.device_brand.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #f9f9f9;")
        brand_model_layout.addWidget(self.device_brand)
        brand_model_layout.addWidget(QLabel("Model:"))
        self.device_model = QLabel()
        self.device_model.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #f9f9f9;")
        brand_model_layout.addWidget(self.device_model)
        layout.addLayout(brand_model_layout)
        
        # Serial number (read-only, from selected device)
        layout.addWidget(QLabel("Serial Number:"))
        self.device_serial = QLabel()
        self.device_serial.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #f9f9f9;")
        layout.addWidget(self.device_serial)
        
        # Customer issue
        layout.addWidget(QLabel("Customer Reported Issue:"))
        self.customer_issue = QTextEdit()
        self.customer_issue.setMinimumHeight(70)
        layout.addWidget(self.customer_issue)
        
        # Description
        layout.addWidget(QLabel("Repair Description (Optional):"))
        self.description = QTextEdit()
        self.description.setMinimumHeight(70)
        layout.addWidget(self.description)
        
        # Priority
        layout.addWidget(QLabel("Priority:"))
        self.priority = QComboBox()
        self.priority.addItems(["LOW", "NORMAL", "HIGH", "URGENT"])
        layout.addWidget(self.priority)
        
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
    
    def on_customer_changed(self):
        """Load customer devices when customer changes"""
        try:
            customer_id = self.customer_combo.currentData()
            
            # Block signals while populating to avoid triggering on_device_changed
            self.device_combo.blockSignals(True)
            self.device_combo.clear()
            self.device_combo.addItem("-- Select Device --", None)
            
            if not customer_id:
                self._clear_device_display()  # Only clear display fields, not combo
                self.device_combo.blockSignals(False)
                return
            
            # Load customer's devices
            try:
                devices = Database.execute_query(
                    "SELECT id, device_type_id, brand, model, serial_number FROM devices WHERE customer_id = ? ORDER BY id DESC",
                    (customer_id,)
                )
            except Exception as e:
                AppLogger.error(f"Error loading devices for customer {customer_id}: {e}")
                devices = []
            
            for device in devices:
                display_text = f"{device['brand']} {device['model']}" if device['brand'] else "Device"
                self.device_combo.addItem(display_text, device['id'])
            
            # Re-enable signals
            self.device_combo.blockSignals(False)
            self._clear_device_display()  # Only clear display fields
        except Exception as e:
            AppLogger.error(f"Error in on_customer_changed: {e}")
            self.device_combo.blockSignals(False)
    
    def on_device_changed(self):
        """Load device details when device is selected"""
        device_id = self.device_combo.currentData()
        if not device_id:
            self.clear_device_info()
            return
        
        # Load device details
        devices = Database.execute_query(
            "SELECT device_type_id, brand, model, serial_number FROM devices WHERE id = ?",
            (device_id,)
        )
        
        try:
            if devices:
                device = dict(devices[0]) if hasattr(devices[0], 'keys') else devices[0]
                self.device_brand.setText(device.get('brand', '') or '')
                self.device_model.setText(device.get('model', '') or '')
                self.device_serial.setText(device.get('serial_number', '') or '')
                self._device_type_id = device.get('device_type_id')
                # Set device type label if available
                if self._device_type_id:
                    try:
                        dt_result = Database.execute_query("SELECT name FROM device_types WHERE id = ?", (self._device_type_id,))
                        if dt_result:
                            self.device_type_label.setText(dt_result[0]['name'])
                        else:
                            self.device_type_label.setText("")
                    except Exception as e:
                        AppLogger.error(f"Error loading device type: {e}")
                        self.device_type_label.setText("")
                else:
                    self.device_type_label.setText("")
            else:
                self._clear_device_display()
        except Exception as e:
            AppLogger.error(f"Error in on_device_changed: {e}")
            self._clear_device_display()
    
    def _clear_device_display(self):
        """Clear device display fields (not the combo list)"""
        self.device_brand.setText("")
        self.device_model.setText("")
        self.device_serial.setText("")
        self.device_type_label.setText("")
        self._device_type_id = None
    
    def clear_device_info(self):
        """Clear device information and combo (for backwards compat)"""
        self.device_combo.clear()
        self.device_combo.addItem("-- Select Device --", None)
        self._clear_device_display()
    
    def accept(self):
        """Create ticket"""
        if not self.customer_combo.currentData():
            QMessageBox.warning(self, "Error", "Customer required")
            return
        
        if not self.device_combo.currentData():
            QMessageBox.warning(self, "Error", "Device required")
            return
        
        try:
            customer_id = self.customer_combo.currentData()
            device_id = self.device_combo.currentData()
            
            # Combine customer issue and description for ticket description
            combined_description = self.customer_issue.toPlainText().strip()
            if self.description.toPlainText().strip():
                combined_description += "\n\n" + self.description.toPlainText().strip()
            
            if not combined_description:
                QMessageBox.warning(self, "Error", "Please provide a description or customer issue")
                return
            
            # Create ticket with all device details
            ticket_id = RepairService.create_ticket(
                customer_id=customer_id,
                device_id=device_id,
                priority=self.priority.currentText(),
                description=combined_description,
                device_type_id=getattr(self, '_device_type_id', None),
                device_brand=self.device_brand.text(),
                device_model=self.device_model.text(),
                device_serial=self.device_serial.text(),
                customer_issue=self.customer_issue.toPlainText().strip()
            )
            
            if ticket_id:
                QMessageBox.information(self, "Success", f"Ticket created successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to create ticket")
                return
            
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save ticket: {str(e)}")
            AppLogger.error(f"Ticket save error: {e}")
            import traceback
            traceback.print_exc()


class TicketDetailDialog(QDialog):
    """View/edit ticket details"""
    
    def __init__(self, ticket_id: int, parent):
        super().__init__(parent)
        self.ticket_id = ticket_id
        try:
            self.ticket = RepairService.get_ticket(ticket_id)
            if not self.ticket:
                raise Exception(f"Ticket {ticket_id} not found")
            self.setWindowTitle(f"Ticket {self.ticket.get('ticket_number', 'Unknown')}")
        except Exception as e:
            print(f"Error loading ticket: {e}")
            import traceback
            traceback.print_exc()
            raise
        self.setGeometry(200, 100, 900, 800)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog with tabs"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create tabs
        tabs = QTabWidget()
        
        # Details tab
        details_widget = self.create_details_tab()
        tabs.addTab(details_widget, "Details")
        
        # Repair Items tab
        items_widget = self.create_items_tab()
        tabs.addTab(items_widget, "Repair Items")
        
        # Notes tab
        notes_widget = self.create_notes_tab()
        tabs.addTab(notes_widget, "Notes")
        
        main_layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def create_details_tab(self):
        """Create details tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Ticket number and status
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel(f"Ticket: {self.ticket['ticket_number']}"))
        top_layout.addStretch()
        top_layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["PENDING", "IN_PROGRESS", "COMPLETED", "UNREPAIRABLE", "CANCELLED"])
        self.status_combo.setCurrentText(self.ticket['status'])
        top_layout.addWidget(self.status_combo)
        layout.addLayout(top_layout)
        
        # Customer
        layout.addWidget(QLabel("Customer:"))
        customer = CustomerService.get_customer(self.ticket['customer_id'])
        customer_name = customer['name'] if customer else f"Customer #{self.ticket['customer_id']}"
        layout.addWidget(QLabel(customer_name))
        
        # Device info
        layout.addWidget(QLabel("Device Type:"))
        self.device_type_combo = QComboBox()
        types = Database.execute_query("SELECT id, name FROM device_types ORDER BY name")
        for device_type in types:
            self.device_type_combo.addItem(device_type['name'], device_type['id'])
        if self.ticket.get('device_type_id'):
            for i in range(self.device_type_combo.count()):
                if self.device_type_combo.itemData(i) == self.ticket['device_type_id']:
                    self.device_type_combo.setCurrentIndex(i)
                    break
        layout.addWidget(self.device_type_combo)
        
        # Device brand and model
        brand_model_layout = QHBoxLayout()
        brand_model_layout.addWidget(QLabel("Brand:"))
        self.device_brand = QLineEdit()
        self.device_brand.setText(self.ticket.get('device_brand', '') or '')
        brand_model_layout.addWidget(self.device_brand)
        brand_model_layout.addWidget(QLabel("Model:"))
        self.device_model = QLineEdit()
        self.device_model.setText(self.ticket.get('device_model', '') or '')
        brand_model_layout.addWidget(self.device_model)
        layout.addLayout(brand_model_layout)
        
        # Device serial
        layout.addWidget(QLabel("Device Serial Number:"))
        self.device_serial = QLineEdit()
        self.device_serial.setText(self.ticket.get('device_serial', '') or '')
        layout.addWidget(self.device_serial)
        
        # Customer issue
        layout.addWidget(QLabel("Customer Reported Issue:"))
        self.customer_issue = QTextEdit()
        self.customer_issue.setText(self.ticket.get('customer_issue', '') or '')
        self.customer_issue.setMinimumHeight(60)
        layout.addWidget(self.customer_issue)
        
        # Description
        layout.addWidget(QLabel("Repair Description:"))
        self.description = QTextEdit()
        self.description.setText(self.ticket['description'])
        self.description.setMinimumHeight(60)
        layout.addWidget(self.description)
        
        # Fault found
        layout.addWidget(QLabel("Fault Found:"))
        self.fault_found = QTextEdit()
        self.fault_found.setText(self.ticket.get('fault_found', '') or '')
        self.fault_found.setMinimumHeight(60)
        layout.addWidget(self.fault_found)
        
        # Priority
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Priority:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["LOW", "NORMAL", "HIGH", "URGENT"])
        self.priority_combo.setCurrentText(self.ticket['priority'])
        priority_layout.addWidget(self.priority_combo)
        priority_layout.addStretch()
        layout.addLayout(priority_layout)
        
        # Completed status
        complete_layout = QHBoxLayout()
        self.completed_check = QCheckBox("Mark as Completed")
        self.completed_check.setChecked(self.ticket['status'] == 'COMPLETED')
        complete_layout.addWidget(self.completed_check)
        complete_layout.addStretch()
        layout.addLayout(complete_layout)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_items_tab(self):
        """Create repair items management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Items table
        layout.addWidget(QLabel("Repair Items:"))
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels(["Service", "Quantity", "Unit Price", "Subtotal", "Notes", "Actions"])
        header = self.items_table.horizontalHeader()
        header.setStretchLastSection(False)
        for i in range(5):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        make_table_read_only(self.items_table)
        
        # Add item button
        add_item_btn = QPushButton("Add Repair Item")
        add_item_btn.clicked.connect(self.add_repair_item)
        
        # Totals
        totals_layout = QHBoxLayout()
        totals_layout.addStretch()
        totals_layout.addWidget(QLabel("Total:"))
        self.items_total_label = QLabel(f"{get_currency_symbol(get_app_currency())}0.00")
        self.items_total_label.setStyleSheet("font-weight: bold;")
        totals_layout.addWidget(self.items_total_label)
        
        layout.addWidget(self.items_table)
        layout.addWidget(add_item_btn)
        layout.addLayout(totals_layout)
        layout.addStretch()
        widget.setLayout(layout)
        
        # Load items into table
        self.reload_items_tab()
        
        return widget
    
    def reload_items_tab(self):
        """Reload repair items table without recreating the widget"""
        self.repair_items = Database.execute_query(
            """SELECT ri.id, ri.service_id, rs.category_id, rs.name, ri.quantity, ri.unit_price, ri.subtotal, ri.notes
               FROM repair_items ri
               JOIN repair_services rs ON ri.service_id = rs.id
               WHERE ri.repair_ticket_id = ?
               ORDER BY ri.created_at""",
            (self.ticket_id,)
        )
        
        self.items_table.setRowCount(len(self.repair_items))
        symbol = get_currency_symbol(get_app_currency())
        for row, item in enumerate(self.repair_items):
            item_dict = dict(item) if hasattr(item, 'keys') else item
            self.items_table.setItem(row, 0, QTableWidgetItem(item_dict['name']))
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item_dict['quantity'])))
            self.items_table.setItem(row, 2, QTableWidgetItem(f"{symbol}{item_dict['unit_price']:.2f}"))
            self.items_table.setItem(row, 3, QTableWidgetItem(f"{symbol}{item_dict['subtotal']:.2f}"))
            self.items_table.setItem(row, 4, QTableWidgetItem(item_dict.get('notes', '') or ''))
            
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(50)
            edit_btn.clicked.connect(lambda checked, iid=item_dict['id'], r=row: self.edit_repair_item(iid, r))
            action_layout.addWidget(edit_btn)
            
            remove_btn = QPushButton("Remove")
            remove_btn.setMaximumWidth(60)
            remove_btn.clicked.connect(lambda checked, iid=item_dict['id']: self.remove_repair_item(iid))
            action_layout.addWidget(remove_btn)
            
            action_layout.addStretch()
            action_widget.setLayout(action_layout)
            self.items_table.setCellWidget(row, 5, action_widget)
        
        self.update_items_total()
    
    def add_repair_item(self):
        """Open dialog to add a new repair item"""
        dialog = AddRepairItemDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['service_id']:
                QMessageBox.warning(self, "Error", "Please select a service")
                return
            try:
                Database.execute_update(
                    """INSERT INTO repair_items (repair_ticket_id, service_id, quantity, unit_price, subtotal, notes, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
                    (self.ticket_id, data['service_id'], data['quantity'], data['unit_price'], data['subtotal'], data['notes'])
                )
                self.reload_items_tab()
                QMessageBox.information(self, "Success", "Repair item added successfully")
            except Exception as e:
                AppLogger.error(f"Error adding repair item: {e}")
                QMessageBox.critical(self, "Error", f"Failed to add item: {str(e)}")
    
    def edit_repair_item(self, item_id: int, row_idx: int):
        """Open dialog to edit a repair item"""
        item = Database.execute_query(
            """SELECT ri.id, ri.service_id, rs.category_id, ri.quantity, ri.unit_price, ri.notes
               FROM repair_items ri
               JOIN repair_services rs ON ri.service_id = rs.id
               WHERE ri.id = ?""",
            (item_id,)
        )
        
        if not item:
            QMessageBox.warning(self, "Error", "Item not found")
            return
        
        item_row = dict(item[0]) if hasattr(item[0], 'keys') else item[0]
        item_data = {
            'id': item_id,
            'service_id': item_row['service_id'],
            'category_id': item_row['category_id'],
            'quantity': item_row['quantity'],
            'unit_price': item_row['unit_price'],
            'notes': item_row.get('notes', '') or ''
        }
        
        dialog = AddRepairItemDialog(self, item_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['service_id']:
                QMessageBox.warning(self, "Error", "Please select a service")
                return
            try:
                Database.execute_update(
                    """UPDATE repair_items SET service_id = ?, quantity = ?, unit_price = ?, subtotal = ?, notes = ?
                       WHERE id = ?""",
                    (data['service_id'], data['quantity'], data['unit_price'], data['subtotal'], data['notes'], item_id)
                )
                self.reload_items_tab()
                QMessageBox.information(self, "Success", "Repair item updated successfully")
            except Exception as e:
                AppLogger.error(f"Error updating repair item: {e}")
                QMessageBox.critical(self, "Error", f"Failed to update item: {str(e)}")
    
    def remove_repair_item(self, item_id: int):
        """Remove a repair item"""
        if QMessageBox.question(self, "Confirm", "Remove this repair item?") == QMessageBox.StandardButton.Yes:
            try:
                Database.execute_update("DELETE FROM repair_items WHERE id = ?", (item_id,))
                self.reload_items_tab()
            except Exception as e:
                AppLogger.error(f"Error removing repair item: {e}")
                QMessageBox.critical(self, "Error", f"Failed to remove item: {str(e)}")
    
    def update_items_total(self):
        """Update the total of all repair items"""
        total = sum(float(dict(item).get('subtotal', 0) if hasattr(item, 'keys') else item['subtotal']) for item in self.repair_items)
        symbol = get_currency_symbol(get_app_currency())
        self.items_total_label.setText(f"{symbol}{total:.2f}")
    
    def create_notes_tab(self):
        """Create notes tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Notes table
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(3)
        self.notes_table.setHorizontalHeaderLabels(["Type", "Note", "Actions"])
        header = self.notes_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(3):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        make_table_read_only(self.notes_table)
        layout.addWidget(self.notes_table)
        
        # Add note section
        layout.addWidget(QLabel("Add Note:"))
        add_note_layout = QHBoxLayout()
        add_note_layout.addWidget(QLabel("Type:"))
        self.note_type_combo = QComboBox()
        self.note_type_combo.addItems(["CUSTOMER_ISSUE", "TECHNICIAN_NOTES", "FAULT_FOUND"])
        add_note_layout.addWidget(self.note_type_combo)
        add_note_layout.addStretch()
        layout.addLayout(add_note_layout)
        
        self.note_text = QTextEdit()
        self.note_text.setMinimumHeight(80)
        layout.addWidget(self.note_text)
        
        add_note_btn = QPushButton("Add Note")
        add_note_btn.clicked.connect(self.add_note)
        layout.addWidget(add_note_btn)
        
        widget.setLayout(layout)
        
        # Load initial notes
        self.reload_notes_tab()
        
        return widget
    
    def reload_notes_tab(self):
        """Reload notes table content without recreating the widget"""
        notes = Database.execute_query(
            "SELECT id, note_type, note FROM ticket_notes WHERE repair_ticket_id = ? ORDER BY created_at DESC",
            (self.ticket_id,)
        )
        
        self.notes_table.setRowCount(len(notes))
        for row, note in enumerate(notes):
            note_dict = dict(note) if hasattr(note, 'keys') else note
            note_type = note_dict.get('note_type', 'TECHNICIAN_NOTES') or 'TECHNICIAN_NOTES'
            self.notes_table.setItem(row, 0, QTableWidgetItem(note_type))
            self.notes_table.setItem(row, 1, QTableWidgetItem(note_dict.get('note', '') or ''))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, nid=note_dict['id']: self.delete_note(nid))
            self.notes_table.setCellWidget(row, 2, delete_btn)
    
    def add_note(self):
        """Add a note"""
        if not self.note_text.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Note text required")
            return
        try:
            Database.execute_update(
                """INSERT INTO ticket_notes (repair_ticket_id, user_id, note_type, note, created_at)
                   VALUES (?, ?, ?, ?, datetime('now'))""",
                (self.ticket_id, AuthService.get_current_user().get('user_id'),
                 self.note_type_combo.currentText(), self.note_text.toPlainText())
            )
            self.note_text.clear()
            self.reload_notes_tab()
        except Exception as e:
            AppLogger.error(f"Error adding note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add note: {str(e)}")
    
    def delete_note(self, note_id):
        """Delete a note"""
        if QMessageBox.question(self, "Confirm", "Delete this note?") == QMessageBox.StandardButton.Yes:
            try:
                Database.execute_update("DELETE FROM ticket_notes WHERE id = ?", (note_id,))
                self.reload_notes_tab()
            except Exception as e:
                AppLogger.error(f"Error deleting note: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete note: {str(e)}")
        """Create notes tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Notes table
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(3)
        self.notes_table.setHorizontalHeaderLabels(["Type", "Note", "Actions"])
        header = self.notes_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(3):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        make_table_read_only(self.notes_table)
        layout.addWidget(self.notes_table)
        
        # Add note section
        layout.addWidget(QLabel("Add Note:"))
        add_note_layout = QHBoxLayout()
        add_note_layout.addWidget(QLabel("Type:"))
        self.note_type_combo = QComboBox()
        self.note_type_combo.addItems(["CUSTOMER_ISSUE", "TECHNICIAN_NOTES", "FAULT_FOUND"])
        add_note_layout.addWidget(self.note_type_combo)
        add_note_layout.addStretch()
        layout.addLayout(add_note_layout)
        
        self.note_text = QTextEdit()
        self.note_text.setMinimumHeight(80)
        layout.addWidget(self.note_text)
        
        add_note_btn = QPushButton("Add Note")
        add_note_btn.clicked.connect(self.add_note)
        layout.addWidget(add_note_btn)
        
        widget.setLayout(layout)
        
        # Load initial notes into table
        self.reload_notes_tab()
        
        return widget
    
    def reload_notes_tab(self):
        """Reload notes table content without recreating the widget"""
        notes = Database.execute_query(
            "SELECT id, note_type, note FROM ticket_notes WHERE repair_ticket_id = ? ORDER BY created_at DESC",
            (self.ticket_id,)
        )
        
        self.notes_table.setRowCount(len(notes))
        for row, note in enumerate(notes):
            note_dict = dict(note) if hasattr(note, 'keys') else note
            note_type = note_dict.get('note_type', 'TECHNICIAN_NOTES') or 'TECHNICIAN_NOTES'
            self.notes_table.setItem(row, 0, QTableWidgetItem(note_type))
            self.notes_table.setItem(row, 1, QTableWidgetItem(note_dict.get('note', '') or ''))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, n_id=note_dict['id']: self.delete_note(n_id))
            self.notes_table.setCellWidget(row, 2, delete_btn)
    
    def add_note(self):
        """Add a note"""
        if not self.note_text.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Note text required")
            return
        
        try:
            Database.execute_update(
                """INSERT INTO ticket_notes (repair_ticket_id, user_id, note_type, note, created_at)
                   VALUES (?, ?, ?, ?, datetime('now'))""",
                (self.ticket_id, AuthService.get_current_user().get('user_id'),
                 self.note_type_combo.currentText(), self.note_text.toPlainText())
            )
            self.note_text.clear()
            self.reload_notes_tab()
        except Exception as e:
            AppLogger.error(f"Error adding note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add note: {str(e)}")
    
    def delete_note(self, note_id):
        """Delete a note"""
        if QMessageBox.question(self, "Confirm", "Delete this note?") == QMessageBox.StandardButton.Yes:
            try:
                Database.execute_update("DELETE FROM ticket_notes WHERE id = ?", (note_id,))
                self.reload_notes_tab()
            except Exception as e:
                AppLogger.error(f"Error deleting note: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete note: {str(e)}")
    
    def save_changes(self):
        """Save all changes"""
        try:
            updates = {
                'status': self.status_combo.currentText(),
                'device_type_id': self.device_type_combo.currentData(),
                'device_brand': self.device_brand.text(),
                'device_model': self.device_model.text(),
                'device_serial': self.device_serial.text(),
                'customer_issue': self.customer_issue.toPlainText(),
                'description': self.description.toPlainText(),
                'fault_found': self.fault_found.toPlainText(),
                'priority': self.priority_combo.currentText()
            }
            
            if self.completed_check.isChecked():
                updates['status'] = 'COMPLETED'
                # Use current timestamp for completed_at - will be handled by SQL
                from datetime import datetime
                updates['completed_at'] = datetime.now().isoformat()
            
            RepairService.update_ticket(self.ticket_id, **updates)
            
            # Reload ticket from database to verify changes were saved
            self.ticket = RepairService.get_ticket(self.ticket_id)
            if not self.ticket:
                raise Exception(f"Failed to reload ticket {self.ticket_id}")
            
            QMessageBox.information(self, "Success", "Ticket updated successfully")
            self.accept()
        except Exception as e:
            AppLogger.error(f"Error saving ticket: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save ticket: {str(e)}")
            import traceback
            traceback.print_exc()


class AddRepairItemDialog(QDialog):
    """Add or edit repair item with category and service selection"""
    
    def __init__(self, parent, item_data=None):
        super().__init__(parent)
        self.item_data = item_data  # For edit mode
        self.setWindowTitle("Add Repair Item" if not item_data else "Edit Repair Item")
        self.setGeometry(200, 100, 500, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Category dropdown
        layout.addWidget(QLabel("Service Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("-- Select Category --", None)
        categories = Database.execute_query(
            "SELECT id, name FROM service_categories ORDER BY name"
        )
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        layout.addWidget(self.category_combo)
        
        # Service dropdown
        layout.addWidget(QLabel("Service:"))
        self.service_combo = QComboBox()
        self.service_combo.addItem("-- Select Service --", None)
        self.service_combo.currentIndexChanged.connect(self.on_service_changed)
        layout.addWidget(self.service_combo)
        
        # Quantity
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Quantity:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setValue(1)
        self.qty_spin.valueChanged.connect(self.update_subtotal)
        qty_layout.addWidget(self.qty_spin)
        qty_layout.addStretch()
        layout.addLayout(qty_layout)
        
        # Unit Price
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Unit Price:"))
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setMinimum(0.0)
        self.price_spin.setMaximum(9999.99)
        self.price_spin.setValue(0.0)
        self.price_spin.setDecimals(2)
        self.price_spin.valueChanged.connect(self.update_subtotal)
        price_layout.addWidget(self.price_spin)
        price_layout.addStretch()
        layout.addLayout(price_layout)
        
        # Subtotal (read-only)
        subtotal_layout = QHBoxLayout()
        subtotal_layout.addWidget(QLabel("Subtotal:"))
        self.subtotal_label = QLabel("$0.00")
        self.subtotal_label.setStyleSheet("font-weight: bold;")
        subtotal_layout.addWidget(self.subtotal_label)
        subtotal_layout.addStretch()
        layout.addLayout(subtotal_layout)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_text = QTextEdit()
        self.notes_text.setMinimumHeight(100)
        layout.addWidget(self.notes_text)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Load edit data if provided
        if self.item_data:
            self.load_item_data()
        else:
            self.refresh_services()
    
    def on_category_changed(self):
        """Refresh service list based on selected category"""
        self.refresh_services()
    
    def refresh_services(self):
        """Load services for selected category"""
        category_id = self.category_combo.currentData()
        self.service_combo.clear()
        self.service_combo.addItem("-- Select Service --", None)
        
        if category_id:
            services = Database.execute_query(
                """SELECT id, name, base_price FROM repair_services
                   WHERE category_id = ? ORDER BY name""",
                (category_id,)
            )
            for service in services:
                svc = dict(service) if hasattr(service, 'keys') else service
                display_text = f"{svc['name']} (${svc['base_price']:.2f})"
                self.service_combo.addItem(display_text, svc['id'])
    
    def on_service_changed(self):
        """Update unit price when service is selected"""
        service_id = self.service_combo.currentData()
        if service_id:
            service = Database.execute_query(
                "SELECT base_price FROM repair_services WHERE id = ?",
                (service_id,)
            )
            if service:
                svc = dict(service[0]) if hasattr(service[0], 'keys') else service[0]
                self.price_spin.setValue(float(svc['base_price']))
        else:
            self.price_spin.setValue(0.0)
    
    def update_subtotal(self):
        """Calculate and update subtotal"""
        subtotal = self.qty_spin.value() * self.price_spin.value()
        self.subtotal_label.setText(f"${subtotal:.2f}")
    
    def load_item_data(self):
        """Load existing item data for editing"""
        if not self.item_data:
            return
        
        # Set category
        if self.item_data.get('category_id'):
            for i in range(self.category_combo.count()):
                if self.category_combo.itemData(i) == self.item_data['category_id']:
                    self.category_combo.setCurrentIndex(i)
                    break
        
        # Set service
        if self.item_data.get('service_id'):
            for i in range(self.service_combo.count()):
                if self.service_combo.itemData(i) == self.item_data['service_id']:
                    self.service_combo.setCurrentIndex(i)
                    break
        
        # Set quantity and price
        self.qty_spin.setValue(self.item_data.get('quantity', 1))
        self.price_spin.setValue(float(self.item_data.get('unit_price', 0.0)))
        
        # Set notes
        self.notes_text.setText(self.item_data.get('notes', '') or '')
        
        self.update_subtotal()
    
    def get_data(self):
        """Return form data"""
        return {
            'service_id': self.service_combo.currentData(),
            'category_id': self.category_combo.currentData(),
            'service_name': self.service_combo.currentText().split('(')[0].strip() if self.service_combo.currentData() else '',
            'quantity': self.qty_spin.value(),
            'unit_price': self.price_spin.value(),
            'subtotal': self.qty_spin.value() * self.price_spin.value(),
            'notes': self.notes_text.toPlainText()
        }
