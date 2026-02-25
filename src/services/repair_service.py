"""
Repair Service - Repair ticket and service management
"""

from typing import List, Dict, Optional
from datetime import datetime
from src.services.database import Database


class RepairService:
    """Repair ticket management"""
    
    @staticmethod
    def _generate_ticket_number() -> str:
        """Generate unique ticket number"""
        import time
        timestamp = int(time.time() * 1000) % 1000000
        return f"TKT-{timestamp}"
    
    @staticmethod
    def create_ticket(customer_id: int, device_id: Optional[int] = None,
                     description: str = "", priority: str = "NORMAL",
                     assigned_to: Optional[int] = None,
                     device_type_id: Optional[int] = None,
                     device_brand: str = "",
                     device_model: str = "",
                     device_serial: str = "",
                     customer_issue: str = "",
                     fault_found: str = "") -> Optional[int]:
        """Create repair ticket with all details"""
        if not customer_id or not description.strip():
            return None
        
        ticket_number = RepairService._generate_ticket_number()
        query = '''
            INSERT INTO repair_tickets
            (ticket_number, customer_id, device_id, description, priority, assigned_to,
             device_type_id, device_brand, device_model, device_serial, customer_issue, fault_found)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        Database.execute_update(query, (
            ticket_number, customer_id, device_id, description, priority, assigned_to,
            device_type_id, device_brand, device_model, device_serial, customer_issue, fault_found
        ))
        
        result = Database.execute_query(
            "SELECT id FROM repair_tickets WHERE ticket_number = ?",
            (ticket_number,)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def get_ticket(ticket_id: int) -> Optional[Dict]:
        """Get ticket by ID"""
        result = Database.execute_query(
            "SELECT * FROM repair_tickets WHERE id = ?",
            (ticket_id,)
        )
        return dict(result[0]) if result else None
    
    @staticmethod
    def list_tickets(status: Optional[str] = None) -> List[Dict]:
        """List tickets, optionally filtered by status"""
        if status:
            results = Database.execute_query(
                "SELECT * FROM repair_tickets WHERE status = ? ORDER BY created_at DESC",
                (status,)
            )
        else:
            results = Database.execute_query(
                "SELECT * FROM repair_tickets ORDER BY created_at DESC"
            )
        return [dict(row) for row in results]
    
    @staticmethod
    def update_ticket(ticket_id: int, **kwargs) -> bool:
        """Update ticket"""
        allowed_fields = {
            'description', 'status', 'priority', 'assigned_to', 'completed_at',
            'device_id', 'device_type_id', 'device_brand', 'device_model', 
            'device_serial', 'customer_issue', 'fault_found'
        }
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not fields or not ticket_id:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        query = f"UPDATE repair_tickets SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        Database.execute_update(query, tuple(fields.values()) + (ticket_id,))
        return True
    
    @staticmethod
    def add_note(ticket_id: int, user_id: int, note: str) -> Optional[int]:
        """Add note to ticket"""
        if not note.strip():
            return None
        
        query = '''
            INSERT INTO ticket_notes (repair_ticket_id, user_id, note)
            VALUES (?, ?, ?)
        '''
        Database.execute_update(query, (ticket_id, user_id, note))
        result = Database.execute_query(
            "SELECT id FROM ticket_notes WHERE repair_ticket_id = ? AND user_id = ? ORDER BY id DESC LIMIT 1",
            (ticket_id, user_id)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def get_notes(ticket_id: int) -> List[Dict]:
        """Get ticket notes"""
        results = Database.execute_query(
            "SELECT * FROM ticket_notes WHERE repair_ticket_id = ? ORDER BY created_at",
            (ticket_id,)
        )
        return [dict(row) for row in results]
    
    @staticmethod
    def add_item(ticket_id: int, service_id: int, quantity: int = 1, 
                unit_price: float = 0, notes: str = "") -> Optional[int]:
        """Add service item to ticket"""
        subtotal = quantity * unit_price
        query = '''
            INSERT INTO repair_items 
            (repair_ticket_id, service_id, quantity, unit_price, subtotal, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        Database.execute_update(query, (ticket_id, service_id, quantity, unit_price, subtotal, notes))
        result = Database.execute_query(
            "SELECT id FROM repair_items WHERE repair_ticket_id = ? ORDER BY id DESC LIMIT 1",
            (ticket_id,)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def get_ticket_items(ticket_id: int) -> List[Dict]:
        """Get items in ticket"""
        results = Database.execute_query(
            "SELECT * FROM repair_items WHERE repair_ticket_id = ?",
            (ticket_id,)
        )
        return [dict(row) for row in results]
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        """Delete item from ticket"""
        Database.execute_update("DELETE FROM repair_items WHERE id = ?", (item_id,))
        return True


class ServiceCatalog:
    """Repair services catalog"""
    
    @staticmethod
    def create_service(name: str, category: str = "", base_price: float = 0, 
                      description: str = "") -> Optional[int]:
        """Create new service"""
        if not name.strip():
            return None
        
        query = '''
            INSERT INTO repair_services (name, category, base_price, description)
            VALUES (?, ?, ?, ?)
        '''
        Database.execute_update(query, (name, category, base_price, description))
        result = Database.execute_query(
            "SELECT id FROM repair_services WHERE name = ? ORDER BY id DESC LIMIT 1",
            (name,)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def list_services() -> List[Dict]:
        """List all services"""
        results = Database.execute_query("SELECT * FROM repair_services ORDER BY name")
        return [dict(row) for row in results]
    
    @staticmethod
    def get_service(service_id: int) -> Optional[Dict]:
        """Get service by ID"""
        result = Database.execute_query(
            "SELECT * FROM repair_services WHERE id = ?",
            (service_id,)
        )
        return dict(result[0]) if result else None
    
    @staticmethod
    def update_service(service_id: int, **kwargs) -> bool:
        """Update service"""
        allowed_fields = {'name', 'category', 'base_price', 'description'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not fields or not service_id:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        query = f"UPDATE repair_services SET {set_clause} WHERE id = ?"
        Database.execute_update(query, tuple(fields.values()) + (service_id,))
        return True
    
    @staticmethod
    def delete_service(service_id: int) -> bool:
        """Delete service"""
        Database.execute_update("DELETE FROM repair_services WHERE id = ?", (service_id,))
        return True
