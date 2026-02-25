# 🚀 RepairQ 2.0 - Quick Start Guide

## Installation

1. **Download:** `dist/RepairQ.exe`
2. **Run:** Double-click the file
3. **Done!** No installation or prerequisites needed

---

## First Time Setup

### Step 1: Login
- **Username:** `admin`
- **Password:** `admin`

### Step 2: Change Password
- You will be forced to change the default password
- Enter a strong password
- Click "Change Password"

### Step 3: Start Using
- You now have full access to the application
- Head to **Admin Panel** to:
  - Add users (Staff/Technician)
  - Add repair services and pricing
  - Configure company information
  - Manage device types

---

## Main Features

### 📊 Dashboard
Quick overview of pending tickets, active work, and completed repairs

### 🔧 Repair Tickets
- Create and manage repair work orders
- Track status and priority
- Add service items and notes
- Link to customers and devices

### 👥 Customers
- Complete customer database
- Contact information management
- Search and filtering
- Notes and history

### 🖥️ Devices
- Track customer devices
- Device types (Laptop, Desktop, Printer, etc.)
- Serial numbers and models
- Link to customers

### 💰 Invoices
- Generate invoices from repair tickets
- Track payment status
- Calculate totals with tax

### ⚙️ Admin Panel
- **Users:** Create and manage staff accounts
- **Repair Services:** Build your service catalog with pricing
- **Settings:** Company info, tax rate, currency
- **Device Types:** Manage device categories

---

## Default Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |

**Important:** Change this password on first login!

---

## User Roles

### Admin
- Full system access
- User management
- Configure settings
- View all data

### Staff
- Create and manage repair tickets
- Customer management
- Invoice generation
- View reports

### Technician
- Create and update tickets
- View invoices
- Limited to assigned work

---

## Database

The application automatically creates a database file (`repairq.db`) on first run.
- No manual setup required
- Stored in the application folder
- All data is local - no cloud dependency

---

## Common Tasks

### Create a New Repair Ticket
1. Go to **Repair Tickets** tab
2. Click **New Ticket**
3. Select customer and device
4. Enter description and priority
5. Click **Create**

### Add a Customer
1. Go to **Customers** tab
2. Click **New Customer**
3. Fill in contact information
4. Click **Save**

### Add a Repair Service
1. Go to **Admin Panel**
2. Click **Repair Services** tab
3. Click **Add Service**
4. Enter name and pricing
5. Click **Add**

### Generate an Invoice
1. Go to **Invoices** tab
2. Click **New Invoice**
3. Select a repair ticket
4. Enter amounts
5. Click **Create**

---

## System Requirements

- **OS:** Windows 10 or Windows 11
- **Architecture:** 64-bit (x64)
- **RAM:** 2 GB minimum
- **Storage:** 100 MB free space
- **Display:** 1024x768 minimum resolution

---

## Support Files

- **APPLICATION_GUIDE.md** - Complete user and developer guide
- **COMPLETION_SUMMARY.md** - Project overview and statistics
- **repairq.db** - SQLite database file

---

## Troubleshooting

### Application won't start
- Ensure Windows 10/11 is running
- Try right-click → Run as Administrator
- Delete `repairq.db` for a clean restart

### Forgot admin password
- Delete `repairq.db` file
- Restart the application
- Login with `admin` / `admin` again

### Can't create users
- Make sure you're logged in as Admin
- Go to Admin Panel → Users tab
- Click "Add User"

---

## Tips & Tricks

- Use **Dashboard** for daily overview
- **admin/admin** is the default - change it immediately
- **Admin Panel** is only visible to Admin users
- All data is **automatically saved** to the database
- **No backup button?** Database file is in application folder

---

## Version Information

- **Version:** 2.0.0
- **Release Date:** 2024
- **Platform:** Windows 10/11 x64
- **File Size:** 36.6 MB

---

## Getting Help

Refer to **APPLICATION_GUIDE.md** for:
- Detailed feature documentation
- Architecture overview
- Deployment information
- Development guide

---

**Ready to go!** 🎉

Launch `RepairQ.exe` and start managing your repair business.

---
