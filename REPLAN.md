# RepairQ - Complete Application Replan

## Current Issues

❌ Login screen not responsive - buttons hidden
❌ No password change requirement on first login
❌ All features showing "Coming Soon"
❌ No admin panel for system setup
❌ No data management screens
❌ No permission/role system
❌ Not truly modular
❌ No icon pack integration

## New Architecture

### 1. Module Structure

```
src/
├── main.py                          # Entry point
├── config.py                        # Configuration & constants
├── ui/
│   ├── __init__.py
│   ├── styles.py                    # Centralized styling
│   ├── components/
│   │   ├── __init__.py
│   │   ├── tables.py               # Reusable table widget
│   │   ├── dialogs.py              # Reusable dialogs
│   │   └── navbar.py               # Navigation bar
│   ├── windows/
│   │   ├── __init__.py
│   │   ├── login_window.py         # Login + password change
│   │   └── main_window.py          # Main app window
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py             # Dashboard
│       ├── admin_panel.py           # Admin setup
│       │   ├── customers.py
│       │   ├── repair_items.py
│       │   ├── users.py
│       │   └── settings.py
│       ├── repairs.py               # Repair tickets
│       ├── devices.py               # Device tracking
│       ├── services.py              # Service management
│       └── invoices.py              # Invoice generation
├── services/
│   ├── __init__.py
│   ├── database.py                 # Database operations
│   ├── auth.py                     # Authentication & roles
│   ├── customer_service.py         # Customer operations
│   ├── repair_service.py           # Repair operations
│   └── invoice_service.py          # Invoice operations
├── models/
│   ├── __init__.py
│   └── models.py                   # Data models
├── utils/
│   ├── __init__.py
│   ├── helpers.py                  # Utility functions
│   └── icons.py                    # Icon management
└── database/
    ├── __init__.py
    └── repairq.db                  # SQLite database
```

### 2. Core Features to Implement

#### A. Authentication & Security
- [x] User login
- [ ] First-time password change (REQUIRED)
- [ ] Password hashing (BCrypt)
- [ ] User roles (Admin, Staff, Technician)
- [ ] Permission system
- [ ] Session management

#### B. Admin Panel
- [ ] Customer Management
  - Add/Edit/Delete customers
  - View customer history
  - Contact information
- [ ] Repair Items Setup
  - Define repair service types
  - Pricing
  - Category management
- [ ] User Management
  - Create users
  - Assign roles
  - Permission assignment
  - Change user status
- [ ] System Settings
  - Company info
  - Logo/branding
  - Email settings
  - Invoice templates

#### C. Core Operations
- [ ] Repair Ticket Management
  - Create tickets
  - Assign to technicians
  - Track status
  - Add notes
- [ ] Device Management
  - Register devices
  - Track repairs per device
  - Warranty tracking
- [ ] Invoice Management
  - Generate invoices
  - Track payments
  - PDF export
  - Email invoices

#### D. Dashboard
- [ ] Statistics
  - Outstanding repairs
  - Revenue metrics
  - Customer count
  - Recent activity

### 3. UI/UX Requirements

- [ ] Fully responsive layout
- [ ] Maximize/Minimize/Close window controls
- [ ] Proper button spacing and sizing
- [ ] Icon integration (icon_pack.ico)
- [ ] Professional color scheme
- [ ] Proper form layouts
- [ ] Data validation
- [ ] Status messages/notifications
- [ ] Modal dialogs for actions

### 4. Database Schema

Tables needed:
- users (id, username, password_hash, role, email, status, created_at)
- customers (id, name, phone, email, address, notes, created_at)
- devices (id, type, brand, model, serial, customer_id)
- repair_services (id, name, category, price, description)
- repair_tickets (id, customer_id, device_id, description, status, priority, assigned_to, created_at, completed_at)
- repair_items (repair_ticket_id, service_id, quantity, unit_price, subtotal)
- invoices (id, repair_ticket_id, total_amount, status, created_at, paid_at)
- permissions (id, role, permission_name)
- settings (key, value)

### 5. Development Plan

**Phase 1: Foundation** (Foundation)
- Restructure project with proper modules
- Create responsive base window
- Implement proper login with first-time password change
- Set up role-based access control

**Phase 2: Admin Panel** (Setup)
- Customer management CRUD
- Repair items setup
- User management
- System settings

**Phase 3: Operations** (Core Features)
- Repair ticket management
- Device tracking
- Invoice generation

**Phase 4: Polish** (Finalization)
- Dashboard with statistics
- Reporting
- Icon integration
- Testing & optimization

## Implementation Strategy

Each module is **independent and testable**
Each UI page has **complete CRUD operations**
Database **fully normalized** with proper relationships
All forms **validated and responsive**
Proper **error handling and user feedback**

---

**Goal:** Professional, complete repair shop management application ready for production.
