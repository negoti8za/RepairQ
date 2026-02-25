"""
Authentication Service - User validation and role management
"""

from typing import Optional, Dict, List
from src.services.database import Database, ROLE_ADMIN, ROLE_STAFF, ROLE_TECHNICIAN
from src.utils.logger import AppLogger


class AuthService:
    """Authentication and authorization service"""
    
    # Role permissions
    PERMISSIONS = {
        ROLE_ADMIN: {
            'manage_users', 'manage_customers', 'manage_devices', 'manage_services',
            'create_tickets', 'edit_tickets', 'view_reports', 'manage_settings',
            'view_invoices', 'edit_invoices', 'delete_tickets'
        },
        ROLE_STAFF: {
            'manage_customers', 'create_tickets', 'edit_tickets', 'view_invoices',
            'edit_invoices', 'view_reports'
        },
        ROLE_TECHNICIAN: {
            'create_tickets', 'edit_tickets', 'view_invoices'
        }
    }
    
    _current_user: Optional[Dict] = None
    
    @classmethod
    def login(cls, username: str, password: str) -> tuple[bool, Optional[str], Optional[Dict]]:
        """
        Authenticate user
        Returns: (success, error_message, user_data)
        """
        try:
            if not username.strip() or not password.strip():
                AppLogger.warning(f"Login attempt with empty credentials")
                return False, "Username and password required", None
            
            result = Database.authenticate_user(username, password)
            
            if not result['authenticated']:
                AppLogger.warning(f"Failed login attempt for username: {username}")
                return False, "Invalid username or password", None
            
            user_data = {k: v for k, v in result.items() if k != 'authenticated'}
            cls._current_user = user_data
            AppLogger.info(f"User logged in: {username}, Role: {user_data.get('role')}")
            return True, None, user_data
        except Exception as e:
            AppLogger.error(f"Authentication error for user {username}: {e}")
            return False, "Authentication error", None
    
    @classmethod
    def logout(cls):
        """Clear current user session"""
        if cls._current_user:
            AppLogger.info(f"User logged out: {cls._current_user.get('username', 'Unknown')}")
        cls._current_user = None
    
    @classmethod
    def get_current_user(cls) -> Optional[Dict]:
        """Get currently logged-in user"""
        return cls._current_user
    
    @classmethod
    def has_permission(cls, permission: str) -> bool:
        """Check if current user has permission"""
        if not cls._current_user:
            return False
        
        role = cls._current_user.get('role')
        return permission in cls.PERMISSIONS.get(role, set())
    
    @classmethod
    def can_manage_users(cls) -> bool:
        return cls.has_permission('manage_users')
    
    @classmethod
    def can_manage_customers(cls) -> bool:
        return cls.has_permission('manage_customers')
    
    @classmethod
    def can_manage_services(cls) -> bool:
        return cls.has_permission('manage_services')
    
    @classmethod
    def can_view_reports(cls) -> bool:
        return cls.has_permission('view_reports')
    
    @classmethod
    def is_admin(cls) -> bool:
        """Check if user is admin"""
        if not cls._current_user:
            return False
        return cls._current_user.get('role') == ROLE_ADMIN
    
    @classmethod
    def change_password(cls, user_id: int, new_password: str) -> bool:
        """Update user password"""
        if not new_password or len(new_password) < 3:
            return False
        return Database.update_password(user_id, new_password)
