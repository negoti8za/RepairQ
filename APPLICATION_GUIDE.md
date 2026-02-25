# RepairQ 2.0 - Complete Application Guide

## ✅ Status: PRODUCTION-READY

RepairQ is a complete, modern Windows 10/11 desktop application for managing repair shop operations. It features a responsive UI, comprehensive database, and full suite of business features.

---

## 🚀 Quick Start

### Run the Application

Simply execute the `.exe` file from the `dist/` folder:

```bash
dist/RepairQ.exe
```

**No prerequisites required** - everything is bundled.

### Default Login

- **Username:** `admin`
- **Password:** `admin`

On first login, you will be **forced to change your password** for security.

---

## 📋 Features Implemented

### ✅ User Authentication & Security
- Secure login system with password hashing
- Password change enforcement on first login
- Role-based access control (Admin, Staff, Technician)
- Session management

### ✅ Complete Database
- **9 database tables** with full schema:
  - Users (with roles and permissions)
  - Customers (full contact info)
  - Devices (type, brand, model, serial)
  - Repair Services (catalog of services)
  - Repair Tickets (main work units)
  - Repair Items (line items in tickets)
  - Ticket Notes (history and communication)
  - Invoices (billing and payments)
  - Settings (app configuration)

### ✅ Full-Featured UI (Responsive & Modern)

#### Login Window
- Professional login interface
- Forced password change on first login
- Form validation and error messages
- Responsive design (resizes properly)

#### Main Application Window
- Responsive tabbed interface
- Header with user information
- Menu bar with File and Help menus
- Status bar
- Responsive to window resizing/maximizing

#### Dashboard Page
- Statistics cards (Pending, Active, Completed tickets, Total customers)
- Recent activity feed
- Quick overview of shop status

#### Repair Tickets Page
- View all repair tickets
- Create new tickets with customer, device, priority
- Update ticket status (Pending → In Progress → Completed)
- Add notes and service items to tickets
- Table with full actions (View, Edit)

#### Customers Page
- Complete customer management (CRUD)
- Search and filter customers
- Full contact information (name, phone, email, address, city, state, zip)
- Customer notes
- Edit and delete operations

#### Devices Page
- Device tracking and management
- Device types (Laptop, Desktop, Printer, etc.)
- Brand, model, and serial number tracking
- Link devices to customers
- Create and delete operations

#### Invoices Page
- Invoice generation from repair tickets
- Calculate totals (subtotal, tax, total)
- Track invoice status (Pending, Sent, Paid, Cancelled)
- Invoice management

#### Admin Panel (4 Tabs)
1. **Users Tab**
   - Create new users with roles
   - View all users
   - Delete users
   - Role assignment (Admin, Staff, Technician)

2. **Repair Services Tab**
   - Manage service catalog
   - Add repair service types with pricing
   - Edit and delete services
   - Base price management

3. **Settings Tab**
   - Configure company info (name, phone, email, address)
   - Tax rate settings
   - Currency configuration
   - All settings stored in database

4. **Device Types Tab**
   - Manage device type catalog
   - Add new device types
   - Delete device types

---

## 🏗️ Project Architecture

```
src/
├── main.py                    # Application entry point
├── config.py                  # Constants, colors, roles, settings
├── __init__.py
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── database.py           # Database connection and schema
│   ├── auth.py               # Authentication and authorization
│   ├── customer_service.py   # Customer CRUD operations
│   ├── repair_service.py     # Repair tickets and services
│   └── invoice_service.py    # Invoice management
└── ui/                        # User interface layer
    ├── __init__.py
    ├── login_window.py       # Login interface
    ├── main_window.py        # Main application window
    └── pages/                # Feature pages
        ├── __init__.py
        ├── dashboard.py      # Overview and statistics
        ├── repairs.py        # Repair ticket management
        ├── customers.py      # Customer management
        ├── devices.py        # Device tracking
        ├── invoices.py       # Invoice management
        └── admin_panel.py    # Admin setup interface
```

### Separation of Concerns
- **Database Layer (`database.py`):** All SQLite operations
- **Service Layer (`*_service.py`):** Business logic and rules
- **UI Layer (`ui/`):** User interface only
- **Config Layer (`config.py`):** Constants and configuration

---

## 🎨 UI Design

- **Modern Windows 11 Style:** Native look and feel
- **Professional Color Scheme:**
  - Primary Blue: `#0078D4`
  - Success Green: `#107C10`
  - Warning Orange: `#FFB900`
  - Danger Red: `#E81123`
- **Responsive Layouts:** Works with window resizing/maximizing
- **Built-in Icons:** From `custom_icon_pack.ico` (114 KB)
- **Font:** Segoe UI (Windows native)

---

## 💾 Database

**File:** `repairq.db` (SQLite 3)

### Tables
1. `users` - User accounts with roles
2. `customers` - Customer information
3. `device_types` - Categories of devices
4. `devices` - Customer devices
5. `repair_services` - Service catalog
6. `repair_tickets` - Main work tickets
7. `repair_items` - Line items in tickets
8. `ticket_notes` - Notes and history
9. `invoices` - Billing records
10. `settings` - Application configuration

### Default Data
- **Admin User:** username `admin`, password `admin` (must change on first login)
- **Default Settings:** Company info, tax rate (8%), currency (USD)
- **Device Types:** Laptop, Desktop, Printer (auto-created)

---

## 🔐 Security Features

- **Password Hashing:** SHA-256 hashing for stored passwords
- **First Login Enforcement:** Admin must change default password immediately
- **Role-Based Access Control:** Admin/Staff/Technician permissions
- **Secure Session Management:** Clean logout clears session

---

## 🛠️ Technology Stack

- **Language:** Python 3.14
- **GUI Framework:** PyQt6 6.7
- **Database:** SQLite 3 (embedded)
- **Packaging:** PyInstaller (single .exe file)
- **Icon Pack:** 114 KB integrated icon set

---

## 📦 Distribution

### Build Command
```bash
python -m PyInstaller --onefile --windowed --name="RepairQ" --icon="custom_icon_pack.ico" src/main.py
```

### Output
- **File:** `dist/RepairQ.exe` (36.6 MB)
- **Delivery:** Single executable file
- **Installation:** No prerequisites - extract and run
- **Requirements:** Windows 10/11 x64

---

## 🎯 Development Philosophy

The codebase follows these principles:

- **Simplicity:** Clear, straightforward code
- **Readability:** Easy to understand implementation
- **Maintainability:** Modular, independent components
- **Testability:** Business logic separated from UI
- **Performance:** Optimized database queries
- **Security:** Proper input validation and data protection

---

## 📝 Usage Examples

### Creating a Repair Ticket
1. Navigate to **Repair Tickets** tab
2. Click **New Ticket**
3. Select customer and device
4. Enter description and priority
5. Click **Create**

### Managing Customers
1. Go to **Customers** tab
2. Click **New Customer** to add
3. Fill in contact information
4. Click **Save**

### Generating an Invoice
1. Go to **Invoices** tab
2. Click **New Invoice**
3. Select repair ticket
4. Enter subtotal and tax
5. Click **Create**

### Admin Setup
1. Go to **Admin Panel** tab (Admin users only)
2. **Users Tab:** Create new staff/technician users
3. **Repair Services Tab:** Add service types and pricing
4. **Settings Tab:** Configure company information
5. **Device Types Tab:** Manage device categories

---

## 🔄 Future Enhancements (Roadmap)

- [ ] PDF invoice generation and printing
- [ ] Email invoice sending
- [ ] Backup and restore functionality
- [ ] Multi-location support
- [ ] Advanced reporting and analytics
- [ ] Customer portal for ticket status
- [ ] SMS notifications
- [ ] Barcode/QR code device tracking
- [ ] Integration with accounting software

---

## 📞 Support & Issues

For issues or feature requests, refer to the GitHub repository or contact development.

---

## 📄 License

All rights reserved. Zoran Jankov, 2024.

---

## 🎓 Technical Notes

### Why Python + PyQt6?
- **Fast Development:** Python reduces development time significantly
- **Easy to Modify:** Clear, readable code for maintenance
- **Native UI:** PyQt6 provides Windows 11 native appearance
- **Single Executable:** PyInstaller creates standalone .exe files
- **No Java Runtime Needed:** Users don't need to install anything

### Database Schema Design
- **Normalized:** Properly designed to avoid data duplication
- **Relationships:** Foreign keys ensure data integrity
- **Timestamps:** Created and updated timestamps on all records
- **Extensible:** Easy to add new features and tables

### UI Responsiveness
- **QVBoxLayout/QHBoxLayout:** Automatic resizing with window
- **Stretch Factors:** Content adjusts to available space
- **Tab Interface:** Modular pages for easier navigation
- **Modern Styling:** CSS-like stylesheets for professional appearance

---

## ✨ Version Information

- **Application:** RepairQ
- **Version:** 2.0.0
- **Build Date:** 2024
- **Platform:** Windows 10/11 x64
- **Python:** 3.14+
- **PyQt6:** 6.7+

---

**Status: ✅ COMPLETE AND PRODUCTION-READY**

The application is fully functional with all core features implemented. Ready for deployment and use in repair shop operations.
