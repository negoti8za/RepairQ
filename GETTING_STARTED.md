# Getting Started with RepairQ

This guide will help you get RepairQ up and running in minutes.

## 📋 Prerequisites

- Windows 7 or later (64-bit)
- Internet connection (for initial download only)
- 50 MB disk space

## 🚀 Installation

### Step 1: Download
1. Visit [RepairQ Releases](https://github.com/negoti8za/RepairQ/releases)
2. Download the latest `RepairQ.exe`
3. Save to any folder (Desktop, Documents, Program Files, etc.)

### Step 2: First Launch
1. Double-click `RepairQ.exe`
2. Application will start (may take 3-5 seconds)
3. Database is created automatically
4. Default admin user is created

### Step 3: Initial Setup
**Login Screen**
- Username: `admin`
- Password: `admin`

**Password Change** (Required on first launch)
- You'll be prompted to change the default password
- Create a strong password
- Remember it for future logins

## 🔐 First-Time Configuration

### 1. Change Your Password (Mandatory)
After logging in with `admin`/`admin`:
1. Navigate to **Admin Panel** (top menu)
2. Select **User Management**
3. Click **Change Password**
4. Enter new password
5. Save changes

### 2. Create Service Categories (Optional but Recommended)
To add repair services:
1. Go to **Admin Panel** → **Service Catalog**
2. Click **Add Category**
3. Enter category name (e.g., "Electronics", "Software", "Hardware")
4. Save

### 3. Add Repair Services (Optional but Recommended)
Now add services under categories:
1. Admin Panel → **Service Catalog**
2. Under your category, click **Add Service**
3. Fill in:
   - Service Name (e.g., "Screen Replacement")
   - Price
   - Notes (optional)
4. Save

This makes creating repair tickets faster - services will auto-populate with pricing.

### 4. Upload Your Logo (Optional)
To add your business logo:
1. Admin Panel → **Settings**
2. Click **Upload Logo**
3. Select image file
4. Your logo appears on dashboard and invoices

## 📱 Creating Your First Repair Ticket

### Step-by-Step Guide

**1. Open Repairs Tab**
- Click "Repairs" in the main menu

**2. Create New Ticket**
- Click "New Ticket" button

**3. Add Customer**
- Select existing customer from dropdown, OR
- Click "New Customer" to create new
- Fill in: Name, Phone, Email, Address

**4. Select Device**
- Choose customer's device from dropdown, OR
- Click "New Device" to add
- Fill in: Device Type, Brand, Model, Serial Number

**5. Add Repair Items** (NEW in v1.2.0)
- Click "Add Repair Item"
- **Select Category** → Services from that category appear
- **Select Service** → Price auto-fills
- **Set Quantity** → If multiple units
- **Add Notes** (optional)
- Subtotal calculates automatically
- Click "Add"

**Add More Items**
- Repeat step 5 for each service needed
- Total updates automatically

**6. Save Ticket**
- Click "Save Ticket"
- Receive confirmation message
- Ticket now appears in Repairs list

## 📄 Creating an Invoice

**From a Repair Ticket:**
1. Go to **Invoices** tab
2. Click **New Invoice**
3. Select the repair ticket
4. Review all items and total
5. Click **Save Invoice**
6. Print or Save As PDF

**Features:**
- Professional layout with your logo
- Company information
- Itemized services with pricing
- Subtotal and total automatically calculated
- Customer contact information

## 👥 Managing Users

### Create New User (Admin Only)
1. Admin Panel → **User Management**
2. Click **Add User**
3. Enter:
   - Username
   - Password
   - Role (Admin, Staff, Technician)
4. Click **Save**

### User Roles
- **Admin**: Full access to all features and settings
- **Staff**: Can manage tickets, customers, devices
- **Technician**: Can view and update repair items only

### Change Password (Any User)
1. Admin Panel → **User Management**
2. Click **Change Password**
3. Enter current and new password
4. Save

## 🎨 Customizing Your Business

### Invoice Customization
1. Admin Panel → **Settings** → **Invoice Customization**
2. Enter:
   - Company Name
   - Address
   - Phone
   - Email
   - Website
   - Footer Text
3. Upload Logo (optional)
4. Save

Your settings appear on all generated invoices.

## 📊 Using the Dashboard

The Dashboard shows:
- **Recent Tickets** - Latest repair orders
- **Quick Stats** - Summary of operations
- **Your Logo** (if uploaded)
- **Quick Actions** - Links to common tasks

Click any ticket to view details.

## 🔍 Finding Information

### Search Customers
1. Go to **Customers** tab
2. Use search box to find by name or phone
3. Click customer to view details and devices

### Search Devices
1. Go to **Devices** tab
2. Filter by customer if needed
3. View all device information

### Search Tickets
1. Go to **Repairs** tab
2. View all repair tickets in list
3. Click to view details, add items, or view status

### Search Invoices
1. Go to **Invoices** tab
2. View all generated invoices
3. Click to view, print, or save

## 🆘 Troubleshooting

### Forgot Admin Password?
**Reset to Defaults:**
1. Close RepairQ
2. Delete `repairq.db` file
3. Restart RepairQ
4. Database recreated with default admin/admin
5. ⚠️ WARNING: All data will be lost!

### Services Not Showing?
**Add Services First:**
1. Admin Panel → Service Catalog
2. Create categories
3. Add services under categories
4. Services now available in repair tickets

### Can't Find Customer/Device?
**Create New Entry:**
1. In New Ticket dialog, use "New Customer" button
2. Or go to Customers tab → "New Customer"
3. Same for devices - use "New Device" button

### Application Won't Start?
**Try These Steps:**
1. Delete `repairq.db` (you'll lose all data)
2. Restart RepairQ
3. Database will be recreated
4. Set up again from scratch

### Invoice Not Printing Correctly?
1. Make sure margins are set correctly
2. Try different paper size
3. Zoom to 100%
4. Try printing to PDF first then to printer

## 💾 Backing Up Your Data

### Manual Backup
1. Close RepairQ
2. Copy `repairq.db` file
3. Save to safe location
4. To restore: Close RepairQ, replace db file, restart

### Recommended Schedule
- Daily if heavy usage
- Weekly if casual usage
- Before major changes
- Before upgrades to new version

## 🆕 New in Version 1.2.0

### Repair Items Feature ✨
- Add multiple services to single ticket
- Each item has quantity and calculated subtotal
- Services auto-populate from catalog
- Category-filtered selection for faster work

### Enhanced Invoices
- All repair items show on invoice
- Line-by-line pricing
- Professional layout maintained

### Code Quality
- Fixed all import issues
- Proper exception handling
- Database operations secure

## 📚 Tips & Best Practices

### Effective Service Setup
1. Create realistic service categories
2. Set accurate pricing
3. Include common services
4. Review quarterly for updates

### Better Ticket Management
1. Add all services before saving ticket
2. Include detailed notes for technician
3. Create invoice before customer leaves
4. Keep customer contact info current

### Business Branding
1. Upload professional logo
2. Keep company info current
3. Customize invoice footer
4. Use consistent branding

### Data Security
1. Change default admin password immediately
2. Use strong passwords
3. Backup database regularly
4. Limit admin access to trusted users

## 🤝 Need Help?

### Documentation
- [Full README](README.md) - Complete feature list
- [Version Notes](VERSION_NOTES.md) - What's new and fixed
- [GitHub Issues](https://github.com/negoti8za/RepairQ/issues) - Known issues

### Getting Support
1. Check [GitHub Issues](https://github.com/negoti8za/RepairQ/issues) - your question may be answered
2. [Create New Issue](https://github.com/negoti8za/RepairQ/issues/new) with:
   - What you were trying to do
   - What happened
   - Error message (if any)
   - Screenshots (if helpful)

### Contact
- **GitHub**: @negoti8za
- **Issues**: [Report Here](https://github.com/negoti8za/RepairQ/issues)

---

## ✅ Checklist: First 30 Minutes

- [ ] Downloaded and installed RepairQ.exe
- [ ] Launched application successfully
- [ ] Logged in with admin/admin
- [ ] Changed admin password
- [ ] Created service categories (optional)
- [ ] Added repair services (optional)
- [ ] Customized business info (optional)
- [ ] Uploaded company logo (optional)
- [ ] Created first customer
- [ ] Created first device
- [ ] Created first repair ticket
- [ ] Added repair items to ticket
- [ ] Generated first invoice

**You're ready to use RepairQ!** 🎉

---

**Last Updated**: February 25, 2026  
**Version**: 1.2.0