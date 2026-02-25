"""
Customer Service - Customer CRUD operations
"""

from typing import List, Dict, Optional
from src.services.database import Database


class CustomerService:
    """Customer management service"""
    
    @staticmethod
    def create_customer(name: str, phone: str = "", email: str = "", 
                       address: str = "", city: str = "", state: str = "", 
                       zip_code: str = "", notes: str = "") -> Optional[int]:
        """Create new customer"""
        if not name.strip():
            return None
        
        query = '''
            INSERT INTO customers 
            (name, phone, email, address, city, state, zip_code, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        Database.execute_update(query, (name, phone, email, address, city, state, zip_code, notes))
        
        # Get the created customer ID
        result = Database.execute_query(
            "SELECT id FROM customers WHERE name = ? ORDER BY id DESC LIMIT 1",
            (name,)
        )
        return result[0]['id'] if result else None
    
    @staticmethod
    def get_customer(customer_id: int) -> Optional[Dict]:
        """Get customer by ID"""
        result = Database.execute_query(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )
        return dict(result[0]) if result else None
    
    @staticmethod
    def list_customers() -> List[Dict]:
        """List all customers"""
        results = Database.execute_query("SELECT * FROM customers ORDER BY name")
        return [dict(row) for row in results]
    
    @staticmethod
    def search_customers(search_term: str) -> List[Dict]:
        """Search customers"""
        query = '''
            SELECT * FROM customers
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        '''
        search = f"%{search_term}%"
        results = Database.execute_query(query, (search, search, search))
        return [dict(row) for row in results]
    
    @staticmethod
    def update_customer(customer_id: int, **kwargs) -> bool:
        """Update customer"""
        if not customer_id or not kwargs:
            return False
        
        allowed_fields = {'name', 'phone', 'email', 'address', 'city', 'state', 'zip_code', 'notes'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not fields:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        query = f"UPDATE customers SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        
        Database.execute_update(query, tuple(fields.values()) + (customer_id,))
        return True
    
    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        """Delete customer"""
        Database.execute_update("DELETE FROM customers WHERE id = ?", (customer_id,))
        return True
