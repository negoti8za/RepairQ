# RepairQ - Desktop Repair Management System

A modern, lightweight desktop application for managing electronics repair services, customers, devices, and invoices. Built with PyQt6 and SQLite for secure, offline-first operation.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### Core Functionality
- **Repair Ticket Management** - Create, track, and manage repair orders with detailed service items
- **Customer Management** - Store and manage customer contact information and device history
- **Device Inventory** - Track devices by customer, type, brand, and model
- **Service Catalog** - Organize services by category with pricing and quick-add functionality
- **Repair Items** - Add detailed service items to tickets with automatic subtotal calculations
- **Invoice Generation** - Create professional invoices from repair tickets with custom branding
- **User Management** - Role-based access control (Admin, Staff, Technician)
- **Admin Panel** - Service management, service categories, settings, and system configuration

### Advanced Features
- **First-Time Setup Wizard** - Default admin user created automatically (`admin`/`admin`)
- **Custom Branding** - Add business logo to invoices and dashboard
- **Invoice Customization** - Company info, contact details, custom footer text
- **Offline Operations** - SQLite database for local-first, no-internet operation
- **Secure Authentication** - Industry-standard password hashing with proper exception handling
- **Currency Support** - 17+ currencies (USD, EUR, GBP, JPY, CAD, AUD, and more)
- **Data Persistence** - Automatic database creation and schema management

## Quick Start

### System Requirements
- Windows 7 or later (64-bit)
- No additional software required (Python and dependencies bundled)
- 50 MB disk space

### Installation

1. **Download the Application**
   - Download `RepairQ.exe` from the [Releases](https://github.com/negoti8za/RepairQ/releases) page
   - Extract to any folder (no installation required)

2. **First Launch**
   ```
   Double-click RepairQ.exe
   ```
   - Database will be created automatically
   - Default admin user created with credentials: `admin` / `admin`
   - You'll be prompted to change the password immediately

3. **Login**
   - Username: `admin`
   - Password: (your new password set on first launch)

### Initial Configuration

1. **Change Admin Password** (Required on first launch)
   - Log in with default credentials
   - Go to Admin Panel → User Management
   - Update your password
   - Save changes

2. **Setup Services** (Recommended)
   - Go to Admin Panel → Service Catalog
   - Add service categories
   - Add repair services with pricing
   - Services are now available when creating repair tickets

3. **Upload Company Logo** (Optional)
   - Go to Admin Panel → Settings
   - Upload your business logo
   - Logo will appear on dashboard and invoices

## How to Use

### Creating a Repair Ticket

1. Go to **Repairs** tab
2. Click **New Ticket**
3. Fill in customer information (select existing or create new)
4. Select customer's device
5. Click **Add Repair Item** to add services:
   - Select service category
   - Service will auto-populate with pricing
   - Set quantity if needed
   - Subtotal calculates automatically
6. Add notes if necessary
7. Click **Save Ticket**

### Managing Repair Items

- **Add Items** - Click "Add Repair Item" in the Repairs Items tab
- **Edit Items** - Select item and click "Edit"
- **Remove Items** - Select item and click "Remove"
- **Total Calculation** - Automatically updates as you add/modify items

### Creating Invoices

1. Go to **Invoices** tab
2. Click **New Invoice**
3. Select repair ticket
4. Review items and total
5. Click **Save Invoice**
6. Print or save as PDF

### Managing Data

#### Customers
- View all customers with contact information
- Track device history per customer
- Edit or delete customer records

#### Devices
- Add new devices per customer
- Track device type, brand, model, and serial number
- View all devices and associated customers

#### Service Catalog (Admin)
- Create service categories
- Add repair services with base pricing
- Edit or delete services
- Services auto-populate in repair tickets

## System Architecture

### Layered Design
```
┌─────────────────────────────────────────────────────┐
│              PyQt6 User Interface                    │
│  (Login, Dashboard, Repairs, Customers, Invoices)  │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│         Service Layer (Business Logic)               │
│ (RepairService, CustomerService, InvoiceService)   │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│         Repository Layer (Data Access)               │
│       (Database Operations & Queries)                │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│            SQLite Database                           │
│      (repairq.db - Created Automatically)           │
└─────────────────────────────────────────────────────┘
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `src/main.py` | Application entry point and main window |
| `src/config.py` | Configuration, constants, and utilities |
| `src/services/` | Business logic layer |
| `src/services/database.py` | Database operations and schema |
| `src/services/auth.py` | Authentication and authorization |
| `src/services/repair_service.py` | Repair ticket management |
| `src/services/customer_service.py` | Customer data operations |
| `src/services/invoice_service.py` | Invoice generation |
| `src/ui/` | User interface components |
| `src/ui/pages/` | Individual feature pages |

### Database Schema

**Tables:**
- `users` - User accounts and roles
- `customers` - Customer information
- `devices` - Device records per customer
- `device_types` - Device type categories
- `repair_tickets` - Repair orders
- `repair_items` - Service items in tickets
- `repair_services` - Available services
- `service_categories` - Service categories
- `invoices` - Generated invoices
- `invoice_customization` - Business branding
- `settings` - Application settings

## Security Features

✓ **Password Hashing** - Industry-standard BCrypt encryption  
✓ **Role-Based Access** - Admin, Staff, and Technician roles  
✓ **Secure Authentication** - Proper exception handling  
✓ **Local Database** - No cloud dependencies or network exposure  
✓ **No Hardcoded Credentials** - Secure credential management  

## Development

### Building from Source

**Prerequisites:**
- Python 3.8 or later
- pip (Python package manager)

**Setup:**
```bash
# Clone repository
git clone https://github.com/negoti8za/RepairQ.git
cd RepairQ

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install PyQt6 reportlab

# Run application
python main.py
```

**Building Executable:**
```bash
# Install PyInstaller
pip install PyInstaller

# Build single-file executable
pyinstaller --onefile --windowed --name RepairQ main.py

# Executable created in: dist/RepairQ.exe
```

### Running Tests
```bash
# Run test suite
python test_repair_items.py

# Expected output: All tests pass
```

### Code Quality
- ✅ All imports validated
- ✅ All method calls verified
- ✅ SQL parameters correct
- ✅ Exception handling proper
- ✅ Code audit passing

## Troubleshooting

### Can't Login
- **Default credentials**: `admin` / `admin` (first launch only)
- **Check database**: Delete `repairq.db` to reset to default state
- **Contact admin**: Ask admin to reset your password

### Repair Item Not Showing in Invoice
- Make sure service is added to ticket items before creating invoice
- Go to ticket → Repairs Items tab → verify items are listed

### Services Not Available
- Go to Admin Panel → Service Catalog
- Create service categories first
- Add services under correct categories

### Database Errors
- Close RepairQ completely
- Delete `repairq.db` file
- Restart RepairQ (new database will be created)

## Performance

- **Startup Time**: < 3 seconds on typical hardware
- **Memory Usage**: ~80 MB base (varies with data size)
- **Executable Size**: 36.8 MB (includes Python runtime)
- **Database**: Optimized for up to 10,000+ tickets

## Version Information

**Current Version**: 1.2.0  
**Release Date**: February 2026  
**Status**: Stable & Production Ready  

See [VERSION_NOTES.md](VERSION_NOTES.md) for detailed changelog and updates.

## Known Limitations

- Windows only (64-bit)
- Single-user at a time per database
- No cloud sync or backup (local database only)
- No multi-database support

## License

MIT License - See LICENSE file for details

## Support

**For Issues & Feedback:**
- [GitHub Issues](https://github.com/negoti8za/RepairQ/issues)
- Create detailed issue with steps to reproduce
- Include error messages and screenshots when applicable

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Push to branch
5. Create Pull Request

## Roadmap

**Planned Features:**
- [ ] Multi-user concurrent access
- [ ] Cloud backup option
- [ ] Invoice templates customization
- [ ] Advanced reporting
- [ ] Email invoice functionality
- [ ] macOS/Linux support
- [ ] Mobile app (iOS/Android)

## Credits

**Created by**: negoti8za  
**Build**: RepairQ Desktop Application  
**Technology Stack**: Python, PyQt6, SQLite, ReportLab  

---

**Latest Release**: [v1.2.0](https://github.com/negoti8za/RepairQ/releases/tag/v1.2.0)  
**Last Updated**: February 25, 2026
- **ORM**: Hibernate JPA
- **Security**: BCrypt password hashing
- **Build Tool**: Maven

## Getting Started

### Quick Start (Windows Desktop)

**Requirements**: Java 21 LTS installed and in PATH

```cmd
REM Run the application
RepairQ-Run.bat

REM Or manually:
java -Xmx512m -jar RepairQ-0.0.1-SNAPSHOT.jar
```

> ⚠️ **Note**: JavaFX requires native libraries. See [WINDOWS-DEPLOYMENT.md](WINDOWS-DEPLOYMENT.md) for solutions if you get "JavaFX runtime components missing" error.

### Building from Source

```bash
# Clone the repository
git clone https://github.com/negoti8za/RepairQ.git
cd RepairQ

# Build with Maven
mvn clean package

# Run the application (requires JavaFX SDK setup)
java -Xmx512m \
  --add-modules javafx.controls,javafx.fxml \
  --module-path /path/to/javafx-sdk-21/lib \
  -jar target/RepairQ-0.0.1-SNAPSHOT.jar

# Or use the batch launcher
RepairQ-Run.bat
```

### Deployment Guide

For detailed deployment instructions, including:
- Running with existing Java installation
- Setting up JavaFX SDK
- Building native Windows installers
- jpackage configuration

👉 See: [WINDOWS-DEPLOYMENT.md](WINDOWS-DEPLOYMENT.md)

## Next Steps

1. Complete migration to JavaFX UI components
2. Implement full user management features
3. Add invoice generation functionality
4. Create native Windows installers with jpackage
5. Add comprehensive testing
