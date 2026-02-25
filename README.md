# RepairQ v2.0.0

**RepairQ** is a Windows desktop application for managing electronics repair shops — tickets, customers, devices, invoices, and billing — built with Python, PyQt6, and SQLite.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Download

| Package | Size | Description |
|---|---|---|
| `RepairQ-Setup-v2.0.0.exe` | ~27 MB | Windows installer — Start Menu + Desktop shortcut |
| `RepairQ-Portable-v2.0.0.zip` | ~37 MB | Portable single `.exe` — no install required |

> Download from the [Releases](https://github.com/negoti8za/RepairQ/releases) page.

No Java, no .NET, no prerequisites — Python runtime is bundled inside the executable.

---

## Features

- **Repair Tickets** — create and track repair orders with status, priority, device details, and fault notes
- **Service Items** — add itemised services to each ticket with quantity and auto-calculated subtotals
- **Customers** — full contact records linked to tickets and devices
- **Devices** — tracked by customer, type, brand, model, and serial number
- **Invoices** — generate A4-fit PDF/print invoices with company logo, customer info, device details, and line items
- **Invoice Customisation** — header, footer, terms & conditions, tax rate, and currency (17+ currencies)
- **Admin Panel** — user management, service catalogue, device types, settings, and invoice customisation
- **Role-based access** — Admin, Staff, and Technician roles
- **Offline-first** — SQLite database stored locally, no internet or cloud required

---

## Quick Start

### First Launch

1. Double-click `RepairQ.exe` (or run the installer)
2. Log in with the default credentials:
   - **Username:** `admin`
   - **Password:** `admin`
3. Change the admin password when prompted

### Recommended Setup (5 minutes)

1. **Admin Panel ? Settings** — enter your company name, address, phone, email, upload logo
2. **Admin Panel ? Invoice Settings** — set header, footer, terms, tax rate and currency
3. **Admin Panel ? Service Catalogue** — add service categories and repair services with pricing
4. Start creating customers, devices, and tickets

---

## Usage

### Repair Tickets

1. **Repairs ? New Ticket**
2. Select or create a customer
3. Select the customer's device (brand/model/serial auto-fill)
4. Set priority and describe the issue
5. **Repair Items tab** — add services from the catalogue; subtotals calculate automatically
6. Add notes as the repair progresses
7. Mark as **COMPLETED** when done

### Invoices

1. **Invoices ? New Invoice** (ticket must be COMPLETED)
2. Select the ticket — services auto-load from repair items
3. Review items, confirm totals
4. **Create Invoice** — then view, print, or save as PDF
5. Update status to SENT / PAID / CANCELLED as needed

---

## Building from Source

**Requirements:** Python 3.8+

```bash
git clone https://github.com/negoti8za/RepairQ.git
cd RepairQ

python -m venv venv
venv\Scripts\activate
pip install PyQt6

python main.py
```

**Build portable EXE:**
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name RepairQ --icon src/resources/icon.ico main.py
# Output: dist/RepairQ.exe
```

**Build Windows installer (requires [NSIS](https://nsis.sourceforge.io)):**
```bash
# 1. Build onedir first
python -m PyInstaller --noconfirm --onedir --windowed --name RepairQ --icon src/resources/icon.ico main.py --distpath dist-dir

# 2. Compile installer
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
# Output: releases/RepairQ-Setup-v2.0.0.exe
```

---

## Project Structure

```
RepairQ/
+-- main.py                     # Entry point
+-- requirements.txt            # Dependencies
+-- installer.nsi               # NSIS installer script
+-- src/
¦   +-- config.py               # Constants, colours, currency helpers
¦   +-- main.py                 # App bootstrap / window stack
¦   +-- services/
¦   ¦   +-- database.py         # Schema creation, migrations, queries
¦   ¦   +-- auth.py             # Login / session management
¦   ¦   +-- repair_service.py   # Ticket CRUD
¦   ¦   +-- customer_service.py # Customer CRUD
¦   ¦   +-- invoice_service.py  # Invoice CRUD
¦   +-- ui/
¦   ¦   +-- login_window.py
¦   ¦   +-- main_window.py      # Tab host + global stylesheet
¦   ¦   +-- pages/
¦   ¦       +-- dashboard.py
¦   ¦       +-- repairs.py
¦   ¦       +-- customers.py
¦   ¦       +-- devices.py
¦   ¦       +-- invoices.py
¦   ¦       +-- admin_panel.py
¦   +-- resources/
¦   ¦   +-- icon.ico
¦   +-- utils/
¦       +-- logger.py
```

---

## Database

SQLite file (`repairq.db`) created automatically on first launch beside the executable.

| Table | Purpose |
|---|---|
| `users` | Accounts and roles |
| `customers` | Customer contacts |
| `devices` | Device records |
| `device_types` | Device categories |
| `repair_tickets` | Repair orders |
| `repair_items` | Itemised services on a ticket |
| `repair_services` | Service catalogue |
| `service_categories` | Service groupings |
| `invoices` | Generated invoices |
| `invoice_customization` | Logo, currency, tax, header/footer/terms |
| `settings` | Company info |
| `ticket_notes` | Repair notes |

> **Reset database:** delete `repairq.db` and restart — a fresh database with the default admin user is created automatically.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Can't log in | Default credentials are `admin` / `admin` on first launch |
| Services not in ticket | Go to Admin ? Service Catalogue and add services with pricing |
| Invoice shows no line items | Add services to the ticket's **Repair Items** tab before creating the invoice |
| Database error | Delete `repairq.db` and restart to rebuild the schema |

---

## Tech Stack

- **Python 3.8+**
- **PyQt6** — UI framework
- **SQLite3** — local database (stdlib)
- **PyInstaller** — packages Python into a single Windows EXE
- **NSIS** — Windows installer

---

## License

MIT — see [LICENSE](LICENSE) for details.

## Contributing

1. Fork ? feature branch ? commit ? pull request
2. [Open an issue](https://github.com/negoti8za/RepairQ/issues) for bugs or feature requests

---

**Version:** 2.0.0 · **Updated:** February 2026 · **Platform:** Windows 64-bit
