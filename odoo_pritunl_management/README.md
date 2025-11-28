# Pritunl VPN Management Module for Odoo

Complete Odoo module for managing Pritunl VPN servers, users, organizations, and subscriptions.

## Installation Guide

### Step 1: Copy Module to Odoo Addons Directory

Copy the entire `odoo_pritunl_management` folder to your Odoo addons directory:

**Option A - Default Odoo Installation:**
```bash
# For Odoo installed in /opt/odoo
sudo cp -r odoo_pritunl_management /opt/odoo/addons/

# Or for custom addons path
sudo cp -r odoo_pritunl_management /path/to/your/odoo/addons/
```

**Option B - Windows Installation:**
```bash
# Copy to Odoo server addons folder
xcopy /E /I odoo_pritunl_management "C:\Program Files\Odoo 16.0\server\addons\odoo_pritunl_management"
```

### Step 2: Update Addons Path (if needed)

Ensure your `odoo.conf` file includes the addons directory:

```ini
[options]
addons_path = /opt/odoo/addons,/path/to/your/custom/addons
```

### Step 3: Restart Odoo Service

```bash
# For Linux/Ubuntu
sudo systemctl restart odoo

# Or if using manual start
sudo service odoo restart

# For Windows - restart the Odoo service from Services
```

### Step 4: Update Apps List

1. Log in to your Odoo instance as Administrator
2. Go to **Apps** menu
3. Click on the **three dots** (⋮) in the top right
4. Select **Update Apps List**
5. Click **Update** in the confirmation dialog

### Step 5: Install the Module

1. In the **Apps** menu, remove the "Apps" filter to show all modules
2. Search for **"Pritunl"** or **"VPN"**
3. Find **"Pritunl VPN Management"** module
4. Click **Install** button

### Step 6: Configure Pritunl Connection

After installation, configure your Pritunl server credentials:

1. Go to **Pritunl VPN → Configuration**
2. Click **Create**
3. Fill in the details:
   - **Name**: Your server name (e.g., "Main VPN Server")
   - **Base URL**: Your Pritunl URL (e.g., `https://vpn1.craftron.co:8447`)
   - **API Token**: Your Pritunl API token
   - **API Secret**: Your Pritunl API secret
   - **Verify SSL**: Check if using valid SSL certificate
   - **Timeout**: Request timeout in seconds (default: 30)
   - **Is Default**: Mark as default configuration
4. Click **Save**
5. Click **Test Connection** to verify credentials

## Module Dependencies

This module requires:
- `base` - Odoo base module
- `mail` - For chatter and activity tracking
- `sale_subscription` - For subscription management (install from Apps if not present)

If `sale_subscription` is not available in your Odoo version, you need to install it first:

1. Go to **Apps**
2. Search for **"Subscription"**
3. Install **"Subscriptions"** module
4. Then install the Pritunl module

## Post-Installation Setup

### 1. Configure Security Groups

Assign users to Pritunl security groups:

1. Go to **Settings → Users & Companies → Users**
2. Select a user
3. Go to **Access Rights** tab
4. Under **Operations** section, assign one of:
   - **Pritunl User**: Read-only access
   - **Pritunl Manager**: Full management (users, servers)
   - **Pritunl Administrator**: Full configuration access

### 2. Initial Data Sync

Sync existing data from Pritunl server:

1. Go to **Pritunl VPN → Configuration**
2. Open your configuration
3. Click **Sync All Data** button
4. This will import:
   - All organizations
   - All users
   - All servers
   - All hosts
   - All links

### 3. Configure Automated Tasks (Cron Jobs)

The module includes two scheduled tasks (they're active by default):

**To verify/configure:**
1. Go to **Settings → Technical → Automation → Scheduled Actions**
2. Find:
   - **Sync Pritunl Data** (runs every 30 minutes)
   - **Check VPN User Subscriptions** (runs every 1 hour)
3. Adjust the schedule if needed

## Usage Guide

### Managing VPN Users

**Create New User:**
1. Go to **Pritunl VPN → VPN Users**
2. Click **Create**
3. Fill in user details:
   - Name, Email
   - Organization
   - Link to Partner (customer)
   - Link to Subscription (optional)
4. Click **Save**
5. User is automatically created in Pritunl server

**Link User to Subscription:**
1. Open a VPN user
2. Set the **Subscription** field
3. The user will be automatically disabled when subscription expires
4. And re-enabled when subscription is renewed

**Manual Enable/Disable:**
1. Open a VPN user
2. Toggle the **Disabled** checkbox
3. Changes sync immediately to Pritunl

### Managing Servers

**Start/Stop/Restart Server:**
1. Go to **Pritunl VPN → Servers**
2. Open a server
3. Click action buttons:
   - **Start Server**
   - **Stop Server**
   - **Restart Server**

**Create New Server:**
1. Go to **Pritunl VPN → Servers**
2. Click **Create**
3. Fill in server configuration
4. Click **Save**
5. Server is created in Pritunl

### Managing Organizations

1. Go to **Pritunl VPN → Organizations**
2. Create/Edit organizations
3. Changes sync automatically with Pritunl

### Customer VPN Access

**Add VPN Access to Customer:**
1. Go to **Contacts**
2. Open a customer/partner
3. Click **VPN Users** smart button (shows count)
4. Or click **Create VPN User** button in the form

## Troubleshooting

### Module Not Appearing in Apps List

1. Check module is in correct addons path
2. Verify `__manifest__.py` exists and is valid
3. Update apps list again
4. Check Odoo logs: `sudo tail -f /var/log/odoo/odoo-server.log`

### Connection Test Fails

1. Verify Base URL is correct (include `https://` and port)
2. Check API Token and Secret are correct
3. Verify SSL certificate if "Verify SSL" is enabled
4. Check firewall allows connection to Pritunl server
5. Test URL in browser: `https://your-server:port`

### Import Errors

If you get import errors like "No module named 'lib.auth'":

1. Verify `lib/` folder exists in module directory
2. Check all Python SDK files are in `lib/` folder
3. Verify `lib/__init__.py` exists
4. Restart Odoo service

### Permission Errors

If users can't access features:

1. Check user has correct security group assigned
2. Go to **Settings → Users & Companies → Users**
3. Edit user → **Access Rights** tab
4. Assign **Pritunl Manager** or **Pritunl Administrator**

### Subscription Auto-Disable Not Working

1. Check cron job is active:
   - **Settings → Technical → Scheduled Actions**
   - Find "Check VPN User Subscriptions"
   - Verify "Active" is checked
2. Check user has subscription linked
3. Verify subscription module is installed
4. Check Odoo logs for errors

## Module Structure

```
odoo_pritunl_management/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── pritunl_config.py          # API configuration
│   ├── pritunl_organization.py    # Organizations
│   ├── pritunl_user.py            # VPN Users
│   ├── pritunl_server.py          # Servers
│   ├── pritunl_host.py            # Hosts
│   ├── pritunl_link.py            # Site-to-Site Links
│   └── res_partner.py             # Customer integration
├── views/
│   ├── pritunl_config_views.xml
│   ├── pritunl_organization_views.xml
│   ├── pritunl_user_views.xml
│   ├── pritunl_server_views.xml
│   ├── pritunl_host_views.xml
│   ├── pritunl_link_views.xml
│   └── pritunl_menu.xml
├── security/
│   ├── security.xml               # Security groups
│   └── ir.model.access.csv        # Access rights
├── data/
│   └── cron.xml                   # Scheduled tasks
└── lib/                           # Python SDK
    ├── __init__.py
    ├── auth.py
    ├── organizations.py
    ├── users.py
    ├── servers.py
    └── ... (other API modules)
```

## Features

- Dynamic API credential management from Odoo UI
- Full user lifecycle management (create, disable, delete)
- Server operations (start, stop, restart)
- Organization management
- Host and link management
- Subscription-based automatic user control
- Customer/Partner VPN access tracking
- Automated synchronization with Pritunl server
- Complete audit trails via Odoo chatter
- Three-tier security model (User, Manager, Administrator)

## Support

For issues or questions:
1. Check Odoo logs: `/var/log/odoo/odoo-server.log`
2. Enable developer mode in Odoo for more debugging info
3. Verify Pritunl API is accessible and credentials are correct

## Version Information

- **Odoo Version**: 16.0+ (compatible with 14.0, 15.0, 16.0, 17.0)
- **License**: LGPL-3
- **Category**: Operations
