"""
Complete Database Module - SQLite operations with full schema
"""

import sqlite3
import hashlib
import os
from datetime import datetime
from pathlib import Path
from src.utils.logger import AppLogger
from src.config import DATABASE_PATH
ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"
ROLE_TECHNICIAN = "TECHNICIAN"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin"


class Database:
    """Complete database interface"""
    
    @classmethod
    def initialize(cls):
        """Initialize database with complete schema"""
        try:
            if not os.path.exists(DATABASE_PATH):
                AppLogger.info(f"Database not found - creating new database at {DATABASE_PATH}")
                cls._create_schema()
                cls._create_default_user()
                cls._create_default_settings()
                cls._create_default_services()
                AppLogger.info("Database initialization completed successfully")
            else:
                AppLogger.info(f"Database loaded from {DATABASE_PATH}")
                # Ensure all tables exist (handles cases where new tables were added after initial creation)
                cls._create_schema()
                cls._create_default_services()
        except Exception as e:
            AppLogger.error(f"Database initialization failed: {e}")
            raise
    
    @classmethod
    def _create_schema(cls):
        """Create all database tables"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'STAFF' CHECK(role IN ('ADMIN', 'STAFF', 'TECHNICIAN')),
                status TEXT DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'INACTIVE')),
                phone TEXT,
                password_changed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Users table ensured")
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Customers table ensured")
        
        # Device Types table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Device types table ensured")
        
        # Devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                brand TEXT,
                model TEXT,
                serial_number TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_type_id) REFERENCES device_types(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        AppLogger.debug("Devices table ensured")
        
        # Service Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Service categories table ensured")
        
        # Repair Services/Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category_id INTEGER,
                category TEXT,
                base_price REAL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES service_categories(id)
            )
        ''')
        AppLogger.debug("Repair services table ensured")
        
        # Repair Tickets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER NOT NULL,
                device_id INTEGER,
                device_type_id INTEGER,
                device_brand TEXT,
                device_model TEXT,
                device_serial TEXT,
                customer_issue TEXT,
                fault_found TEXT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'UNREPAIRABLE', 'CANCELLED')),
                priority TEXT DEFAULT 'NORMAL' CHECK(priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
                assigned_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (device_id) REFERENCES devices(id),
                FOREIGN KEY (device_type_id) REFERENCES device_types(id),
                FOREIGN KEY (assigned_to) REFERENCES users(id)
            )
        ''')
        AppLogger.debug("Repair tickets table ensured")
        
        # Repair Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repair_ticket_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                unit_price REAL,
                subtotal REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repair_ticket_id) REFERENCES repair_tickets(id),
                FOREIGN KEY (service_id) REFERENCES repair_services(id)
            )
        ''')
        AppLogger.debug("Repair items table ensured")
        
        # Ticket Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repair_ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                note_type TEXT DEFAULT 'CUSTOMER_ISSUE' CHECK(note_type IN ('CUSTOMER_ISSUE', 'TECHNICIAN_NOTES', 'FAULT_FOUND')),
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repair_ticket_id) REFERENCES repair_tickets(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        AppLogger.debug("Ticket notes table ensured")
        
        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                repair_ticket_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                subtotal REAL DEFAULT 0,
                tax REAL DEFAULT 0,
                total_amount REAL,
                status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'SENT', 'PAID', 'CANCELLED')),
                paid_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repair_ticket_id) REFERENCES repair_tickets(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        AppLogger.debug("Invoices table ensured")
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                type TEXT DEFAULT 'string',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Settings table ensured")
        
        # Invoice Customization table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_customization (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_logo BLOB,
                invoice_header TEXT,
                invoice_footer TEXT,
                invoice_terms TEXT,
                tax_enabled INTEGER DEFAULT 1,
                tax_rate REAL DEFAULT 0.08,
                currency TEXT DEFAULT 'USD',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        AppLogger.debug("Invoice customization table ensured")
        
        conn.commit()
        conn.close()
    
    @classmethod
    def _create_default_user(cls):
        """Create default admin user"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        password_hash = cls._hash_password(DEFAULT_ADMIN_PASSWORD)
        
        try:
            cursor.execute('''
                INSERT INTO users 
                (username, password_hash, email, first_name, last_name, role, password_changed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (DEFAULT_ADMIN_USERNAME, password_hash, "admin@repairq.local", "Admin", "User", ROLE_ADMIN, 1))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            conn.close()
    
    @classmethod
    def _create_default_settings(cls):
        """Create default settings"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        default_settings = {
            'company_name': ('RepairQ', 'string'),
            'company_phone': ('+1 (555) 123-4567', 'string'),
            'company_email': ('info@repairq.local', 'string'),
            'company_address': ('123 Main St, City, State 12345', 'string'),
            'tax_rate': ('0.08', 'number'),
            'currency': ('USD', 'string'),
        }
        
        for key, (value, type_) in default_settings.items():
            try:
                cursor.execute('''
                    INSERT INTO settings (key, value, type)
                    VALUES (?, ?, ?)
                ''', (key, value, type_))
            except sqlite3.IntegrityError:
                pass
        
        # Create default invoice customization if not exists
        cursor.execute('SELECT COUNT(*) FROM invoice_customization')
        count = cursor.fetchone()[0]
        
        if count == 0:
            try:
                cursor.execute('''
                    INSERT INTO invoice_customization 
                    (tax_enabled, tax_rate, currency, invoice_header, invoice_footer, invoice_terms)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (1, 0.08, 'USD', 'Invoice', 'Thank you for your business', 'Terms and conditions apply'))
                AppLogger.info("Default invoice customization created")
            except sqlite3.Error as e:
                AppLogger.error(f"Error creating default invoice customization: {e}")
        
        conn.commit()
        conn.close()

    @classmethod
    def _create_default_services(cls):
        """Seed default service categories and repair services (runs on every startup, uses INSERT OR IGNORE)"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Default categories with their services: (category_name, [(service_name, price), ...])
        default_data = [
            ("Diagnostics", [
                ("General fault diagnosis", 30.00),
                ("No power / no boot", 35.00),
                ("Liquid damage inspection", 45.00),
                ("Performance assessment", 30.00),
            ]),
            ("Hardware Repairs – Desktop", [
                ("PSU replacement (labour only)", 50.00),
                ("Motherboard repair (board-level)", 120.00),
                ("RAM replacement (labour only)", 40.00),
                ("GPU replacement (labour only)", 60.00),
                ("Case / fan replacement", 45.00),
            ]),
            ("Hardware Repairs – Laptop", [
                ("Screen replacement", 95.00),
                ("Keyboard replacement", 65.00),
                ("Charging port repair", 85.00),
                ("Hinge repair", 75.00),
                ("Battery replacement", 65.00),
            ]),
            ("Hardware Repairs – Mac", [
                ("MacBook screen replacement", 180.00),
                ("Logic board repair", 220.00),
                ("iMac upgrades", 120.00),
            ]),
            ("Data Services", [
                ("Data recovery (HDD/SSD logical)", 120.00),
                ("External drive recovery", 95.00),
                ("Data transfer (old to new PC)", 60.00),
                ("Backup setup", 55.00),
                ("RAID recovery (software level)", 250.00),
            ]),
            ("Software Services", [
                ("Windows install / reinstall", 60.00),
                ("macOS reinstall", 70.00),
                ("Virus / malware removal", 65.00),
                ("Driver fixes", 45.00),
                ("OS upgrades", 55.00),
                ("Software troubleshooting", 50.00),
            ]),
            ("Upgrades", [
                ("SSD upgrade (labour only)", 45.00),
                ("RAM upgrade (labour only)", 40.00),
                ("GPU upgrade (labour only)", 60.00),
                ("CPU upgrade (labour only)", 70.00),
                ("Custom build assembly", 120.00),
            ]),
            ("Mobile / Tablet Repairs", [
                ("iPhone screen replacement", 75.00),
                ("Android screen replacement", 70.00),
                ("Mobile charging port repair", 65.00),
                ("Mobile battery replacement", 55.00),
                ("Tablet repair", 80.00),
            ]),
            ("Business / Managed Services", [
                ("Network setup", 120.00),
                ("Router / firewall install", 150.00),
                ("Office PC setup", 85.00),
                ("Email configuration", 60.00),
                ("Server maintenance (per hour)", 95.00),
                ("On-site support (per hour)", 80.00),
            ]),
            ("Gaming / Custom Builds", [
                ("Custom PC build", 140.00),
                ("RGB setup", 50.00),
                ("Cooling upgrades", 70.00),
                ("Overclock tuning", 85.00),
            ]),
            ("Console Repairs", [
                ("HDMI port repair", 85.00),
                ("Overheating repair (clean + thermal paste)", 65.00),
                ("Console hard drive replacement / upgrade", 95.00),
            ]),
            ("Admin / Non-Repair", [
                ("Bench Fee / Inspection Fee", 30.00),
                ("No Fix – No Fee", 0.00),
                ("Warranty Repair", 0.00),
            ]),
        ]

        for category_name, services in default_data:
            # Insert category (ignore if already exists)
            cursor.execute(
                "INSERT OR IGNORE INTO service_categories (name) VALUES (?)", (category_name,)
            )
            cursor.execute("SELECT id FROM service_categories WHERE name = ?", (category_name,))
            cat_row = cursor.fetchone()
            if not cat_row:
                continue
            cat_id = cat_row[0]

            for service_name, price in services:
                cursor.execute(
                    "INSERT OR IGNORE INTO repair_services (name, category_id, category, base_price) VALUES (?, ?, ?, ?)",
                    (service_name, cat_id, category_name, price)
                )

        conn.commit()
        conn.close()
        AppLogger.debug("Default service categories and services ensured")

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def authenticate_user(cls, username: str, password: str) -> dict:
        """Authenticate user"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        password_hash = cls._hash_password(password)
        
        cursor.execute('''
            SELECT id, username, email, first_name, last_name, role, password_changed
            FROM users
            WHERE username = ? AND password_hash = ? AND status = 'ACTIVE'
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'authenticated': True,
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'first_name': result[3],
                'last_name': result[4],
                'role': result[5],
                'password_changed': bool(result[6]),
            }
        
        return {'authenticated': False}
    
    @classmethod
    def update_password(cls, user_id: int, new_password: str) -> bool:
        """Update user password"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        password_hash = cls._hash_password(new_password)
        cursor.execute('''
            UPDATE users
            SET password_hash = ?, password_changed = 1, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (password_hash, user_id))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @classmethod
    def get_connection(cls):
        """Get database connection"""
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    @classmethod
    def execute_query(cls, query: str, params: tuple = ()) -> list:
        """Execute SELECT query"""
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            AppLogger.error(f"Database query error: {e}\nQuery: {query}")
            raise
    
    @classmethod
    def execute_update(cls, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE"""
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return cursor.rowcount
        except sqlite3.Error as e:
            AppLogger.error(f"Database update error: {e}\nQuery: {query}")
            raise
