"""
Database module - SQLite database operations
"""

import sqlite3
import os
from pathlib import Path
import hashlib


class Database:
    """SQLite database interface for RepairQ"""
    
    DB_PATH = "repairq.db"
    
    @classmethod
    def initialize(cls):
        """Initialize database with schema"""
        if not os.path.exists(cls.DB_PATH):
            cls._create_schema()
            cls._create_default_user()
    
    @classmethod
    def _create_schema(cls):
        """Create database tables"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'USER',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Config table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                brand TEXT,
                model TEXT,
                serial_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Repairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                customer_name TEXT,
                customer_phone TEXT,
                customer_email TEXT,
                description TEXT,
                status TEXT DEFAULT 'PENDING',
                priority TEXT DEFAULT 'MEDIUM',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices(id)
            )
        ''')
        
        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repair_id INTEGER NOT NULL,
                amount REAL,
                status TEXT DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repair_id) REFERENCES repairs(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @classmethod
    def _create_default_user(cls):
        """Create default admin user"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        # Hash password
        password_hash = cls._hash_password("admin")
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', ("admin", password_hash, "ADMIN"))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # User already exists
        finally:
            conn.close()
    
    @classmethod
    def _hash_password(cls, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def authenticate_user(cls, username: str, password: str) -> dict:
        """Authenticate user and return user info"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        password_hash = cls._hash_password(password)
        
        cursor.execute('''
            SELECT id, username, role FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'role': result[2],
                'authenticated': True
            }
        
        return {'authenticated': False}
    
    @classmethod
    def get_connection(cls):
        """Get database connection"""
        conn = sqlite3.connect(cls.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
