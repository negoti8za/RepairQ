"""
Invoices Page - Invoice management and billing
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QTextDocument, QPdfWriter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from src.config import *
from src.services.invoice_service import InvoiceService
from src.services.repair_service import RepairService
from src.services.database import Database
from src.utils.logger import AppLogger


def make_table_read_only(table: QTableWidget) -> None:
    """Make a table read-only (cannot edit cells by clicking)"""
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


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
        # Make columns stretch equally to fill available space
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(5):  # First 5 columns stretch equally
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        header.setSectionResizeMode(5, header.ResizeMode.Stretch)  # Actions column
        # Make table read-only
        make_table_read_only(self.table)
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
            
            # Get currency symbol from database or use default
            try:
                currency_result = Database.execute_query("SELECT currency FROM invoice_customization LIMIT 1")
                if currency_result and len(currency_result) > 0:
                    currency_row = currency_result[0]
                    currency = dict(currency_row)['currency'] if isinstance(currency_row, tuple) else currency_row['currency']
                else:
                    currency = 'USD'
            except Exception:
                currency = 'USD'
            symbol = get_currency_symbol(currency)
            amount = f"{symbol}{invoice['total_amount']:.2f}"
            self.table.setItem(row, 3, QTableWidgetItem(amount))
            
            status_item = QTableWidgetItem(invoice['status'])
            self.table.setItem(row, 4, status_item)
            
            # Actions cell
            btn_container = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)
            
            view_btn = QPushButton("View")
            view_btn.setMaximumWidth(50)
            view_btn.setMaximumHeight(28)
            view_btn.clicked.connect(lambda checked, iid=invoice['id']: self.view_invoice(iid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(60)
            delete_btn.setMaximumHeight(28)
            delete_btn.clicked.connect(lambda checked, iid=invoice['id']: self.delete_invoice(iid))
            
            btn_layout.addWidget(view_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
            btn_container.setLayout(btn_layout)
            self.table.setCellWidget(row, 5, btn_container)
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol - deprecated, use module function"""
        return get_currency_symbol(currency_code)
    
    def create_invoice(self):
        """Create new invoice"""
        dialog = NewInvoiceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ticket_id, items = dialog.get_data()
            if not ticket_id:
                QMessageBox.warning(self, "Error", "Please select a repair ticket")
                return
            if not items:
                QMessageBox.warning(self, "Error", "Please add at least one service item")
                return
            try:
                ticket = RepairService.get_ticket(ticket_id)
                
                # Check if ticket is completed
                if ticket['status'] != 'COMPLETED':
                    QMessageBox.warning(self, "Error", "Cannot invoice - Repair ticket must be marked as COMPLETED")
                    return
                
                # Calculate totals from items
                subtotal = sum(item['subtotal'] for item in items)
                # Load tax rate from settings
                try:
                    tax_result = Database.execute_query("SELECT tax_rate FROM invoice_customization LIMIT 1")
                    if tax_result and len(tax_result) > 0:
                        tax_row = dict(tax_result[0]) if hasattr(tax_result[0], '__getitem__') else tax_result[0]
                        tax_rate = float(tax_row.get('tax_rate', 8)) / 100
                    else:
                        tax_rate = 0.08
                except:
                    tax_rate = 0.08
                tax = round(subtotal * tax_rate, 2)
                InvoiceService.create_invoice(ticket_id, ticket['customer_id'], subtotal, tax)
                self.load_invoices()
                QMessageBox.information(self, "Success", "Invoice created")
            except Exception as e:
                AppLogger.error(f"Error creating invoice: {e}")
                QMessageBox.critical(self, "Error", f"Failed to create invoice: {str(e)}")
    
    def view_invoice(self, invoice_id: int):
        """View invoice details"""
        dialog = InvoiceDetailDialog(invoice_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_invoices()
    
    def delete_invoice(self, invoice_id: int):
        """Delete invoice"""
        reply = QMessageBox.question(self, "Confirm", "Delete invoice?")
        if reply == QMessageBox.StandardButton.Yes:
            InvoiceService.delete_invoice(invoice_id)
            self.load_invoices()


class NewInvoiceDialog(QDialog):
    """Create invoice dialog - select ticket and add service items"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_items = []
        self.setWindowTitle("New Invoice")
        self.setGeometry(200, 100, 700, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Select ticket
        layout.addWidget(QLabel("Select Repair Ticket:"))
        self.ticket_combo = QComboBox()
        self.ticket_combo.addItem("-- Select Ticket --", None)
        tickets = RepairService.list_tickets()
        from src.services.customer_service import CustomerService as _CS
        for ticket in tickets:
            _customer = _CS.get_customer(ticket['customer_id'])
            _cust_name = _customer['name'] if _customer else f"Customer #{ticket['customer_id']}"
            self.ticket_combo.addItem(f"{ticket['ticket_number']} \u2013 {_cust_name}", ticket['id'])
        self.ticket_combo.currentIndexChanged.connect(self.on_ticket_changed)
        layout.addWidget(self.ticket_combo)
        
        # Service items table
        layout.addWidget(QLabel("Service Items:"))
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["Service", "Unit Price", "Quantity", "Subtotal", "Remove"])
        self.items_table.setMinimumHeight(200)
        header = self.items_table.horizontalHeader()
        header.setStretchLastSection(False)
        for i in range(4):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        layout.addWidget(self.items_table)
        
        # Add service item
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Add Service:"))
        self.service_combo = QComboBox()
        self.service_combo.addItem("-- Select Service --", None)
        services = Database.execute_query("SELECT id, name, base_price FROM repair_services ORDER BY name")
        for service in services:
            self.service_combo.addItem(f"{service['name']} ({get_currency_symbol(get_app_currency())}{service['base_price']:.2f})", service['id'])
        add_layout.addWidget(self.service_combo)
        
        add_layout.addWidget(QLabel("Qty:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setValue(1)
        add_layout.addWidget(self.qty_spin)
        
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item)
        add_layout.addWidget(add_btn)
        add_layout.addStretch()
        layout.addLayout(add_layout)
        
        # Totals
        totals_layout = QHBoxLayout()
        totals_layout.addStretch()
        totals_layout.addWidget(QLabel("Subtotal:"))
        self.subtotal_label = QLabel("$0.00")
        totals_layout.addWidget(self.subtotal_label)
        layout.addLayout(totals_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Create Invoice")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_ticket_changed(self):
        """Load ticket's existing items when ticket is selected"""
        ticket_id = self.ticket_combo.currentData()
        self.items_table.setRowCount(0)
        self.selected_items = []
        
        if not ticket_id:
            return
        
        # Load repair_items for this ticket
        items = Database.execute_query(
            """SELECT ri.id, rs.name, ri.unit_price, ri.quantity, ri.subtotal
               FROM repair_items ri
               JOIN repair_services rs ON ri.service_id = rs.id
               WHERE ri.repair_ticket_id = ?""",
            (ticket_id,)
        )
        
        for item in items:
            item_dict = dict(item) if hasattr(item, 'keys') else item
            self.selected_items.append({
                'service_id': item_dict.get('id'),
                'name': item_dict.get('name'),
                'unit_price': item_dict.get('unit_price'),
                'quantity': item_dict.get('quantity'),
                'subtotal': item_dict.get('subtotal')
            })
            self.add_row_to_table(item_dict.get('name'), item_dict.get('unit_price'), item_dict.get('quantity'), item_dict.get('subtotal'))
        
        self.update_totals()
    
    def add_item(self):
        """Add selected service to items"""
        service_id = self.service_combo.currentData()
        if not service_id:
            QMessageBox.warning(self, "Error", "Please select a service")
            return
        
        qty = self.qty_spin.value()
        
        # Get service details
        service = Database.execute_query(
            "SELECT name, base_price FROM repair_services WHERE id = ?",
            (service_id,)
        )[0]
        
        subtotal = service['base_price'] * qty
        
        self.selected_items.append({
            'service_id': service_id,
            'name': service['name'],
            'unit_price': service['base_price'],
            'quantity': qty,
            'subtotal': subtotal
        })
        
        self.add_row_to_table(service['name'], service['base_price'], qty, subtotal)
        self.service_combo.setCurrentIndex(0)
        self.qty_spin.setValue(1)
        self.update_totals()
    
    def add_row_to_table(self, name: str, unit_price: float, qty: int, subtotal: float):
        """Add row to items table"""
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        symbol = get_currency_symbol(get_app_currency())
        self.items_table.setItem(row, 0, QTableWidgetItem(name))
        self.items_table.setItem(row, 1, QTableWidgetItem(f"{symbol}{unit_price:.2f}"))
        self.items_table.setItem(row, 2, QTableWidgetItem(str(qty)))
        self.items_table.setItem(row, 3, QTableWidgetItem(f"{symbol}{subtotal:.2f}"))
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_item(row))
        self.items_table.setCellWidget(row, 4, remove_btn)
    
    def remove_item(self, row: int):
        """Remove item from table"""
        if row < len(self.selected_items):
            self.selected_items.pop(row)
        self.items_table.removeRow(row)
        self.update_totals()
    
    def update_totals(self):
        """Update total amounts"""
        subtotal = sum(item['subtotal'] for item in self.selected_items)
        symbol = get_currency_symbol(get_app_currency())
        self.subtotal_label.setText(f"{symbol}{subtotal:.2f}")
    
    def get_data(self):
        """Get form data - ticket_id and list of items"""
        return self.ticket_combo.currentData(), self.selected_items



class InvoiceDetailDialog(QDialog):
    """View/edit invoice details with print and save options"""
    
    def __init__(self, invoice_id: int, parent):
        super().__init__(parent)
        self.invoice_id = invoice_id
        self.invoice = InvoiceService.get_invoice(invoice_id)
        if not self.invoice:
            QMessageBox.critical(self, "Error", f"Invoice {invoice_id} not found")
            raise Exception(f"Invoice {invoice_id} not found")
        
        self.setWindowTitle(f"Invoice {self.invoice['invoice_number']}")
        self.setGeometry(200, 100, 600, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Get currency symbol from invoice_customization table
        try:
            currency_result = Database.execute_query("SELECT currency FROM invoice_customization LIMIT 1")
            if currency_result and currency_result[0]:
                curr_row = dict(currency_result[0]) if hasattr(currency_result[0], 'keys') else currency_result[0]
                currency = curr_row.get('currency', 'USD')
                if not currency:
                    currency = 'USD'
            else:
                currency = 'USD'
        except Exception as e:
            AppLogger.error(f"Error getting currency: {e}")
            currency = 'USD'
        symbol = self._get_currency_symbol(currency)
        
        # Get ticket number (with safe handling if ticket not found)
        ticket = None
        ticket_number = f"#{self.invoice.get('repair_ticket_id', 0)}"
        try:
            ticket = RepairService.get_ticket(self.invoice.get('repair_ticket_id', 0))
            if ticket:
                ticket_number = ticket.get('ticket_number', ticket_number)
        except Exception as e:
            AppLogger.error(f"Error getting ticket: {e}")
        
        # Get customer name
        from src.services.customer_service import CustomerService
        _customer = CustomerService.get_customer(self.invoice['customer_id'])
        customer_display = _customer['name'] if _customer else f"Customer #{self.invoice['customer_id']}"
        
        # Calculate outstanding amount
        invoice_status = self.invoice.get('status', 'PENDING')
        outstanding = 0 if invoice_status == 'PAID' else self.invoice.get('total_amount', 0)
        
        # Invoice details
        details_text = f"""
Invoice: {self.invoice['invoice_number']}  |  Ticket: {ticket_number}  |  Customer: {customer_display}

Subtotal: {symbol}{self.invoice['subtotal']:.2f}
Tax: {symbol}{self.invoice['tax']:.2f}
Total: {symbol}{self.invoice['total_amount']:.2f}
Outstanding: {symbol}{outstanding:.2f}
"""
        details_label = QLabel(details_text)
        layout.addWidget(details_label)
        
        # Status management with dropdown
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["PENDING", "SENT", "PAID", "CANCELLED"])
        self.status_combo.setCurrentText(invoice_status)
        self.status_combo.currentTextChanged.connect(self.on_status_changed)
        status_layout.addWidget(self.status_combo)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Cancel note (only visible for CANCELLED status)
        self.cancel_note_label = QLabel("Cancellation Reason:")
        self.cancel_note_input = QLineEdit()
        self.cancel_note_input.setPlaceholderText("Reason for cancellation (optional)...")
        cancel_visible = (invoice_status == 'CANCELLED')
        self.cancel_note_input.setVisible(cancel_visible)
        self.cancel_note_label.setVisible(cancel_visible)
        layout.addWidget(self.cancel_note_label)
        layout.addWidget(self.cancel_note_input)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        print_btn = QPushButton("Print")
        print_btn.setMinimumWidth(100)
        print_btn.clicked.connect(self.print_invoice)
        # Disable print if PAID or CANCELLED
        print_btn.setEnabled(invoice_status not in ['PAID', 'CANCELLED'])
        button_layout.addWidget(print_btn)
        
        save_btn = QPushButton("Save as PDF")
        save_btn.setMinimumWidth(100)
        save_btn.clicked.connect(self.save_as_pdf)
        # Disable save if PAID or CANCELLED
        save_btn.setEnabled(invoice_status not in ['PAID', 'CANCELLED'])
        button_layout.addWidget(save_btn)
        
        update_btn = QPushButton("Update Status")
        update_btn.setMinimumWidth(120)
        update_btn.clicked.connect(self.update_status)
        button_layout.addWidget(update_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(100)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Store references for later use in update_status
        self.print_btn = print_btn
        self.save_btn = save_btn
    
    def on_status_changed(self, new_status: str):
        """Show/hide fields based on selected status"""
        self.cancel_note_input.setVisible(new_status == 'CANCELLED')
        self.cancel_note_label.setVisible(new_status == 'CANCELLED')
        
        # Disable print/save buttons if PAID or CANCELLED
        is_final = new_status in ['PAID', 'CANCELLED']
        self.print_btn.setEnabled(not is_final)
        self.save_btn.setEnabled(not is_final)
    
    def update_status(self):
        """Update invoice status"""
        new_status = self.status_combo.currentText()
        try:
            InvoiceService.update_invoice_status(self.invoice_id, new_status)
            
            if new_status == 'CANCELLED' and self.cancel_note_input.text().strip():
                AppLogger.info(f"Invoice {self.invoice_id} cancelled: {self.cancel_note_input.text()}")
            
            QMessageBox.information(self, "Success", f"Invoice status updated to {new_status}")
            self.accept()  # Close dialog - parent will refresh list
        except Exception as e:
            AppLogger.error(f"Error updating invoice status: {e}")
            QMessageBox.critical(self, "Error", f"Failed to update status: {str(e)}")
    
    def print_invoice(self):
        """Print invoice using system printer"""
        try:
            AppLogger.info(f"Printing invoice {self.invoice['invoice_number']}")
            
            # Create printer
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            
            # Show print dialog
            dialog = QPrintDialog(printer, self)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                AppLogger.info(f"Print cancelled for invoice {self.invoice['invoice_number']}")
                return
            
            # Generate invoice HTML and print
            invoice_html = self._generate_invoice_html()
            
            document = QTextDocument()
            document.setHtml(invoice_html)
            document.print(printer)
            
            AppLogger.info(f"Invoice {self.invoice['invoice_number']} sent to printer")
            QMessageBox.information(self, "Success", 
                f"Invoice {self.invoice['invoice_number']} sent to printer")
        except Exception as e:
            AppLogger.error(f"Print failed for invoice {self.invoice['invoice_number']}: {e}")
            QMessageBox.critical(self, "Error", f"Print failed: {str(e)}")
    
    def save_as_pdf(self):
        """Save invoice as PDF with file dialog"""
        try:
            from datetime import datetime
            from PyQt6.QtGui import QPdfWriter
            import os
            
            # Get default filename
            default_filename = f"Invoice_{self.invoice['invoice_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Show save dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Invoice as PDF",
                os.path.join(os.path.expanduser("~"), "Downloads", default_filename),
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if not file_path:
                AppLogger.info(f"Invoice save cancelled")
                return
            
            # Ensure .pdf extension
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'
            
            # Generate PDF
            pdf_writer = QPdfWriter(file_path)
            pdf_writer.setTitle(f"Invoice {self.invoice['invoice_number']}")
            pdf_writer.setCreator("RepairQ")
            
            # Create document with invoice HTML
            document = QTextDocument()
            document.setHtml(self._generate_invoice_html())
            document.print(pdf_writer)
            
            AppLogger.info(f"Invoice {self.invoice['invoice_number']} saved to {file_path}")
            QMessageBox.information(self, "Success", 
                f"Invoice saved successfully to:\n{file_path}")
        except Exception as e:
            AppLogger.error(f"PDF save failed for invoice {self.invoice['invoice_number']}: {e}")
            QMessageBox.critical(self, "Error", f"Save failed: {str(e)}")
    
    def _generate_invoice_html(self) -> str:
        """Generate compact A4-fit HTML invoice with all details, line items, and customization"""
        from src.services.customer_service import CustomerService
        from src.services.repair_service import RepairService

        invoice_dict = dict(self.invoice) if hasattr(self.invoice, 'keys') else self.invoice

        # Customer info
        customer = CustomerService.get_customer(invoice_dict.get('customer_id'))
        customer_name = customer['name'] if customer else 'Unknown Customer'
        customer_phone = (customer.get('phone') or '') if customer else ''
        customer_email = (customer.get('email') or '') if customer else ''
        customer_address = (customer.get('address') or '') if customer else ''

        # Ticket and device info
        ticket = RepairService.get_ticket(invoice_dict.get('repair_ticket_id'))
        ticket_number = ticket['ticket_number'] if ticket else ''
        device_parts = []
        if ticket:
            if ticket.get('device_brand'): device_parts.append(ticket['device_brand'])
            if ticket.get('device_model'): device_parts.append(ticket['device_model'])
            if ticket.get('device_serial'): device_parts.append(f"S/N: {ticket['device_serial']}")
        device_info = ' '.join(device_parts) or 'N/A'

        # Load individual repair line items for this ticket
        ticket_id = invoice_dict.get('repair_ticket_id')
        repair_items = []
        if ticket_id:
            rows = Database.execute_query(
                """SELECT rs.name, ri.unit_price, ri.quantity, ri.subtotal
                   FROM repair_items ri
                   JOIN repair_services rs ON ri.service_id = rs.id
                   WHERE ri.repair_ticket_id = ? ORDER BY ri.id""",
                (ticket_id,)
            )
            repair_items = [dict(r) if hasattr(r, 'keys') else r for r in (rows or [])]

        # Company settings
        company_info = {}
        settings_rows = Database.execute_query(
            "SELECT key, value FROM settings WHERE key IN ('company_name','company_address','company_phone','company_email')"
        )
        if settings_rows:
            for row in settings_rows:
                rd = dict(row) if hasattr(row, 'keys') else row
                company_info[rd.get('key')] = rd.get('value')
        company_name    = company_info.get('company_name', 'RepairQ') or 'RepairQ'
        company_address = company_info.get('company_address', '') or ''
        company_phone   = company_info.get('company_phone', '') or ''
        company_email   = company_info.get('company_email', '') or ''

        # Invoice customization (header, footer, terms, logo, currency)
        cust_rows = Database.execute_query(
            "SELECT currency, company_logo, invoice_header, invoice_footer, invoice_terms FROM invoice_customization LIMIT 1"
        )
        currency = 'USD'; logo_blob = None
        inv_header = ''; inv_footer = 'Thank you for your business!'; inv_terms = ''
        if cust_rows:
            c = dict(cust_rows[0]) if hasattr(cust_rows[0], 'keys') else cust_rows[0]
            currency   = c.get('currency', 'USD') or 'USD'
            logo_blob  = c.get('company_logo')
            inv_header = c.get('invoice_header', '') or ''
            inv_footer = c.get('invoice_footer', '') or 'Thank you for your business!'
            inv_terms  = c.get('invoice_terms', '') or ''

        symbol = self._get_currency_symbol(currency)

        # Logo
        logo_html = ''
        if logo_blob:
            import base64
            logo_html = f'<img src="data:image/png;base64,{base64.b64encode(logo_blob).decode()}" style="max-height:55px;display:block;">'

        # Build line items rows
        item_rows_html = ''
        for item in repair_items:
            name      = item.get('name', 'Service')
            unit      = float(item.get('unit_price', 0))
            qty       = int(item.get('quantity', 1))
            subtotal  = float(item.get('subtotal', unit * qty))
            item_rows_html += f"""
            <tr>
                <td>{name}</td>
                <td style="text-align:center;">{qty}</td>
                <td style="text-align:right;">{symbol}{unit:.2f}</td>
                <td style="text-align:right;">{symbol}{subtotal:.2f}</td>
            </tr>"""
        if not item_rows_html:
            sub = float(invoice_dict.get('subtotal', 0))
            item_rows_html = f"""
            <tr>
                <td>Repair &amp; Service</td>
                <td style="text-align:center;">1</td>
                <td style="text-align:right;">{symbol}{sub:.2f}</td>
                <td style="text-align:right;">{symbol}{sub:.2f}</td>
            </tr>"""

        header_band = f'<div style="text-align:center;font-size:10px;color:#555;margin-bottom:6px;border-bottom:1px solid #ddd;padding-bottom:4px;">{inv_header}</div>' if inv_header else ''
        terms_band  = f'<div style="margin-top:8px;font-size:9px;color:#666;border-top:1px solid #ddd;padding-top:5px;"><strong>Terms &amp; Conditions:</strong><br>{inv_terms}</div>' if inv_terms else ''

        sub_total = float(invoice_dict.get('subtotal', 0))
        tax_total = float(invoice_dict.get('tax', 0))
        grand_total = float(invoice_dict.get('total_amount', 0))

        return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: A4; margin: 12mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Arial, sans-serif; font-size: 10px; color: #333; margin: 0; padding: 0; }}
  .hdr {{ display:table; width:100%; border-bottom:2px solid #333; padding-bottom:8px; margin-bottom:8px; }}
  .hdr-left {{ display:table-cell; vertical-align:top; }}
  .hdr-right {{ display:table-cell; vertical-align:top; text-align:right; width:200px; }}
  h1 {{ margin:0 0 2px 0; font-size:17px; }}
  .co-info {{ font-size:9px; color:#555; line-height:1.5; }}
  .inv-title {{ font-size:26px; font-weight:bold; color:#bbb; }}
  .inv-num {{ font-size:12px; font-weight:bold; margin-top:2px; }}
  .meta {{ display:table; width:100%; margin-bottom:8px; }}
  .meta-col {{ display:table-cell; vertical-align:top; font-size:9px; line-height:1.6; }}
  .meta-col strong {{ display:block; font-size:10px; border-bottom:1px solid #ddd; margin-bottom:3px; }}
  table {{ width:100%; border-collapse:collapse; margin:6px 0; }}
  th {{ background:#f0f0f0; padding:5px 7px; text-align:left; border:1px solid #ddd; font-size:9px; font-weight:bold; }}
  td {{ padding:4px 7px; border:1px solid #ddd; font-size:9px; }}
  .sum-row td {{ background:#f7f7f7; }}
  .tot-row td {{ background:#ddeef8; font-weight:bold; }}
  .footer {{ margin-top:8px; text-align:center; font-size:9px; color:#888; border-top:1px solid #ddd; padding-top:6px; }}
</style>
</head>
<body>
{header_band}
<div class="hdr">
  <div class="hdr-left">
    <h1>{company_name}</h1>
    <div class="co-info">
      {company_address}<br>
      {'Tel: ' + company_phone if company_phone else ''}{' &nbsp;|&nbsp; ' if company_phone and company_email else ''}{'Email: ' + company_email if company_email else ''}
    </div>
  </div>
  <div class="hdr-right">
    {logo_html}
    <div class="inv-title">INVOICE</div>
    <div class="inv-num"># {invoice_dict.get('invoice_number','')}</div>
  </div>
</div>

<div class="meta">
  <div class="meta-col" style="width:38%;">
    <strong>Bill To</strong>
    <b>{customer_name}</b><br>
    {customer_address + '<br>' if customer_address else ''}
    {'Tel: ' + customer_phone + '<br>' if customer_phone else ''}
    {'Email: ' + customer_email if customer_email else ''}
  </div>
  <div class="meta-col" style="width:32%; padding-left:12px;">
    <strong>Device</strong>
    {device_info}<br>
    {'Ticket: ' + ticket_number if ticket_number else ''}
  </div>
  <div class="meta-col" style="width:30%; text-align:right;">
    <strong>Invoice Info</strong>
    Date: {str(invoice_dict.get('created_at',''))[:10]}<br>
    Status: <b>{invoice_dict.get('status','PENDING')}</b>
  </div>
</div>

<table>
  <tr>
    <th style="width:55%;">Description</th>
    <th style="text-align:center;width:8%;">Qty</th>
    <th style="text-align:right;width:17%;">Unit Price</th>
    <th style="text-align:right;width:20%;">Subtotal</th>
  </tr>
  {item_rows_html}
  <tr class="sum-row">
    <td colspan="3" style="text-align:right;"><i>Subtotal</i></td>
    <td style="text-align:right;">{symbol}{sub_total:.2f}</td>
  </tr>
  <tr class="sum-row">
    <td colspan="3" style="text-align:right;"><i>Tax</i></td>
    <td style="text-align:right;">{symbol}{tax_total:.2f}</td>
  </tr>
  <tr class="tot-row">
    <td colspan="3" style="text-align:right;">TOTAL DUE</td>
    <td style="text-align:right;">{symbol}{grand_total:.2f}</td>
  </tr>
</table>

{terms_band}
<div class="footer">{inv_footer}</div>
</body>
</html>"""
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol for currency code"""
        try:
            return get_currency_symbol(currency_code)
        except Exception as e:
            AppLogger.error(f"Error getting currency symbol for {currency_code}: {e}")
            return '$'  # Default to dollar sign if error
