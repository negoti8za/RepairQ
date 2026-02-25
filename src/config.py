"""
Application Configuration - Constants, colors, roles, settings
"""

# Application Info
APP_NAME = "RepairQ"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Zoran Jankov"

# Database
DATABASE_PATH = "repairq.db"

# User Roles
ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"
ROLE_TECHNICIAN = "TECHNICIAN"

# Default Credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin"
FORCE_PASSWORD_CHANGE_ON_FIRST_LOGIN = True

# UI Dimensions
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 600
LOGIN_WINDOW_WIDTH = 500
LOGIN_WINDOW_HEIGHT = 400

# Colors - Windows 11 Modern Style
COLOR_PRIMARY = "#0078D4"        # Windows Blue
COLOR_SECONDARY = "#50E6FF"      # Light Blue
COLOR_SUCCESS = "#107C10"        # Green
COLOR_WARNING = "#FFB900"        # Orange
COLOR_DANGER = "#E81123"         # Red
COLOR_BACKGROUND = "#FFFFFF"    # White
COLOR_SURFACE = "#F3F3F3"       # Light Gray
COLOR_TEXT_PRIMARY = "#323130"  # Dark Gray
COLOR_TEXT_SECONDARY = "#605E5C" # Medium Gray
COLOR_BORDER = "#D2D0CE"        # Border Gray

# Font Configuration
FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 10
FONT_SIZE_HEADING = 14
FONT_SIZE_LARGE = 16
FONT_SIZE_SMALL = 9

# Status Values
STATUS_PENDING = "PENDING"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_COMPLETED = "COMPLETED"
STATUS_CANCELLED = "CANCELLED"

PRIORITY_LOW = "LOW"
PRIORITY_NORMAL = "NORMAL"
PRIORITY_HIGH = "HIGH"
PRIORITY_URGENT = "URGENT"

# Invoice Status
INVOICE_PENDING = "PENDING"
INVOICE_SENT = "SENT"
INVOICE_PAID = "PAID"
INVOICE_CANCELLED = "CANCELLED"

# Paths
ICON_PACK_PATH = "custom_icon_pack.ico"
RESOURCES_PATH = "resources"

# Settings Keys
SETTINGS = {
    'company_name': 'RepairQ',
    'company_phone': '+1 (555) 123-4567',
    'company_email': 'info@repairq.local',
    'company_address': '123 Main St, City, State 12345',
    'tax_rate': 0.08,
    'currency': 'USD',
}

# Pagination
ITEMS_PER_PAGE = 20

# Validation
MIN_PASSWORD_LENGTH = 3
MAX_PASSWORD_LENGTH = 128
