# Quick Installation Instructions

## The module has been fixed to work without sale_subscription dependency!

Follow these steps to install the module:

## Step 1: Restart Odoo Service

```bash
# On Linux:
sudo systemctl restart odoo

# Or
sudo service odoo restart

# On Windows:
# Go to Services (services.msc) and restart the Odoo service
```

## Step 2: Update Apps List in Odoo

1. Login to Odoo as Administrator
2. Go to **Apps** menu
3. Click the **three dots menu (⋮)** in the top right corner
4. Select **Update Apps List**
5. Click **Update** button

## Step 3: Remove any filters and search for the module

1. In the Apps page, click the **X** to remove the "Apps" filter
2. Search for **"Pritunl"** in the search box
3. You should see "Pritunl VPN Management" with **Install** button

## Step 4: Install the module

1. Click **Install** button on "Pritunl VPN Management"
2. Wait for installation to complete

## Step 5: Configure Pritunl Connection

1. Go to **Pritunl VPN → Configuration**
2. Click **Create**
3. Fill in:
   - **Name**: Main VPN Server
   - **Base URL**: https://vpn1.craftron.co:8447
   - **API Token**: oOOhfrao5cfMvQZqwz8zZq5B9J4PAYHe
   - **API Secret**: pn5uOLmsmrepDukeLq6prDOxoxEg59ZH
   - **Verify SSL**: Check if SSL is valid
4. Click **Test Connection** to verify
5. Click **Sync All Data** to import existing data

## Troubleshooting

### If module still shows "Uninstallable"

Check Odoo logs for errors:

```bash
# Linux
sudo tail -f /var/log/odoo/odoo-server.log

# Or
tail -f ~/.odoo/odoo.log
```

### Common Issues:

1. **Missing requests library**:
   ```bash
   pip3 install requests
   ```

2. **Module path issues**: Verify the module is in the correct addons directory

3. **Permission issues**: Ensure Odoo user has read permissions on the module folder
   ```bash
   sudo chown -R odoo:odoo /path/to/addons/odoo_pritunl_management
   sudo chmod -R 755 /path/to/addons/odoo_pritunl_management
   ```

## What was changed?

The module originally required `sale_subscription` module for subscription-based user management. This has been commented out to make the module work independently.

**To enable subscription features later:**

1. Install `sale_subscription` module from Odoo Apps
2. Uncomment subscription-related code in:
   - `models/pritunl_user.py` (subscription fields and methods)
   - `views/pritunl_user_views.xml` (subscription fields in views)
   - `data/cron.xml` (subscription check cron job)
3. Update `__manifest__.py` to add `sale_subscription` in depends
4. Upgrade the module

## Features Available:

- ✅ Dynamic API credentials management
- ✅ Organization management
- ✅ User management (create, delete, enable/disable)
- ✅ Server management (create, start, stop, restart)
- ✅ Host management
- ✅ Link management (site-to-site VPN)
- ✅ Partner integration
- ✅ Automatic synchronization (every 30 minutes)
- ❌ Subscription-based user control (disabled - can be enabled later)

## Need Help?

Check the module README at: `odoo_pritunl_management/README.md`
