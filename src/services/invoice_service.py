"""
Invoice Service - Invoice generation and management
"""

from typing import List, Dict, Optional
from datetime import datetime
from src.services.database import Database


class InvoiceService:
    """Invoice management"""
    
    @staticmethod
    def _generate_invoice_number() -> str:
        """Generate unique invoice number"""
        import time
        timestamp = int(time.time() * 1000) % 1000000
        return f"INV-{timestamp}"
    
    @staticmethod
    def create_invoice(repair_ticket_id: int, customer_id: int, 
                      subtotal: float = 0, tax: float = 0) -> Optional[int]:
        """Create invoice from ticket"""
        total = subtotal + tax
        invoice_number = InvoiceService._generate_invoice_number()
        
        query = '''
            INSERT INTO invoices 
            (invoice_number, repair_ticket_id, customer_id, subtotal, tax, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        Database.execute_update(query, (invoice_number, repair_ticket_id, customer_id, subtotal, tax, total))
        
        result = Database.execute_query(
            "SELECT id FROM invoices WHERE invoice_number = ?",
            (invoice_number,)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def get_invoice(invoice_id: int) -> Optional[Dict]:
        """Get invoice by ID"""
        result = Database.execute_query(
            "SELECT * FROM invoices WHERE id = ?",
            (invoice_id,)
        )
        return dict(result[0]) if result else None
    
    @staticmethod
    def list_invoices(status: Optional[str] = None) -> List[Dict]:
        """List invoices"""
        if status:
            results = Database.execute_query(
                "SELECT * FROM invoices WHERE status = ? ORDER BY created_at DESC",
                (status,)
            )
        else:
            results = Database.execute_query(
                "SELECT * FROM invoices ORDER BY created_at DESC"
            )
        return [dict(row) for row in results]
    
    @staticmethod
    def update_invoice_status(invoice_id: int, status: str) -> bool:
        """Update invoice status"""
        if status not in ['PENDING', 'SENT', 'PAID', 'CANCELLED']:
            return False
        
        paid_at = datetime.now().isoformat() if status == 'PAID' else None
        query = '''
            UPDATE invoices
            SET status = ?, paid_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        Database.execute_update(query, (status, paid_at, invoice_id))
        return True
    
    @staticmethod
    def calculate_total(ticket_id: int) -> Dict[str, float]:
        """Calculate ticket totals"""
        items = Database.execute_query(
            "SELECT subtotal FROM repair_items WHERE repair_ticket_id = ?",
            (ticket_id,)
        )
        
        subtotal = sum(item['subtotal'] for item in items)
        tax_rate = 0.08  # TODO: Load from settings
        tax = round(subtotal * tax_rate, 2)
        total = round(subtotal + tax, 2)
        
        return {
            'subtotal': subtotal,
            'tax': tax,
            'tax_rate': tax_rate,
            'total': total
        }
    
    @staticmethod
    def delete_invoice(invoice_id: int) -> bool:
        """Delete invoice"""
        Database.execute_update("DELETE FROM invoices WHERE id = ?", (invoice_id,))
        return True
