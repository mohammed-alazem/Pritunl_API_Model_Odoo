# Pritunl API Python SDK

Professional Python SDK for Pritunl VPN Server API with complete HMAC-SHA256 authentication and comprehensive endpoint coverage.

## Features

- ✅ Complete API coverage (120+ endpoints)
- ✅ HMAC-SHA256 authentication
- ✅ Type hints and comprehensive docstrings
- ✅ Easy integration with Odoo and other Python applications
- ✅ Production-ready error handling
- ✅ Organized by functional modules

## Installation

### Prerequisites

```bash
pip install requests
```

### Setup

1. Copy the `python_scripts` folder to your project
2. Configure your credentials in `config.py`:

```python
BASE_URL = "https://vpn1.craftron.co:8447"
API_TOKEN = "your_api_token_here"
API_SECRET = "your_api_secret_here"
```

## Quick Start

### Basic Usage

```python
from python_scripts import organizations, users, servers

# List all organizations
orgs = organizations.list_organizations()
for org in orgs:
    print(f"Organization: {org['name']} (ID: {org['id']})")

# Create a new user
user = users.create_user(
    org_id='507f1f77bcf86cd799439011',
    name='john.doe',
    email='john@example.com',
    groups=['developers']
)
print(f"Created user: {user['id']}")

# Start a VPN server
servers.start_server('507f1f77bcf86cd799439011')
```

### Using Custom Client

```python
from python_scripts.auth import PritunlAuth
from python_scripts import organizations

# Create a custom client with different credentials
client = PritunlAuth(
    base_url="https://vpn2.example.com",
    api_token="different_token",
    api_secret="different_secret"
)

# Use the custom client
orgs = organizations.list_organizations(client=client)
```

## Complete API Reference

### Organizations

```python
from python_scripts import organizations

# List organizations
orgs = organizations.list_organizations()

# Get specific organization
org = organizations.get_organization(org_id='507f...')

# Create organization
org = organizations.create_organization(name='Engineering Team')

# Update organization
org = organizations.update_organization(org_id='507f...', name='New Name')

# Delete organization
organizations.delete_organization(org_id='507f...')

# Find by name
org = organizations.find_organization_by_name('Engineering Team')

# Get or create
org = organizations.get_or_create_organization('Sales Team')
```

### Users

```python
from python_scripts import users

# List users in organization
user_list = users.list_users(org_id='507f...')

# Get specific user
user = users.get_user(org_id='507f...', user_id='507f...')

# Create user
user = users.create_user(
    org_id='507f...',
    name='john.doe',
    email='john@example.com',
    pin='123456',
    groups=['developers', 'vpn-users'],
    disabled=False
)

# Create multiple users
users_list = users.create_multiple_users(
    org_id='507f...',
    users=[
        {'name': 'user1', 'email': 'user1@example.com'},
        {'name': 'user2', 'email': 'user2@example.com'}
    ]
)

# Update user
user = users.update_user(
    org_id='507f...',
    user_id='507f...',
    email='newemail@example.com',
    groups=['developers', 'admins']
)

# Delete user
users.delete_user(org_id='507f...', user_id='507f...')

# Generate OTP secret
otp = users.generate_otp_secret(org_id='507f...', user_id='507f...')
print(f"OTP Secret: {otp['secret']}")

# Get user audit log
logs = users.get_user_audit_log(org_id='507f...', user_id='507f...')

# Device management
users.approve_device(org_id='507f...', user_id='507f...', device_id='device123')
users.delete_device(org_id='507f...', user_id='507f...', device_id='device123')

# Find user by name
user = users.find_user_by_name(org_id='507f...', name='john.doe')

# Get or create user
user = users.get_or_create_user(
    org_id='507f...',
    name='john.doe',
    email='john@example.com'
)
```

### Servers

```python
from python_scripts import servers

# List servers
server_list = servers.list_servers()

# Get specific server
server = servers.get_server(server_id='507f...')

# Create server
server = servers.create_server(
    name='Production VPN',
    network='10.0.0.0/8',
    port=15500,
    protocol='udp',
    dh_param_bits=2048,
    dns_servers=['8.8.8.8', '8.8.4.4'],
    max_clients=2048
)

# Update server
server = servers.update_server(
    server_id='507f...',
    name='Updated Server Name',
    max_clients=4096
)

# Delete server
servers.delete_server(server_id='507f...')

# Server operations
servers.start_server(server_id='507f...')
servers.stop_server(server_id='507f...')
servers.restart_server(server_id='507f...')

# Organization management
orgs = servers.get_server_organizations(server_id='507f...')
servers.attach_organization(server_id='507f...', org_id='507f...')
servers.detach_organization(server_id='507f...', org_id='507f...')

# Route management
routes = servers.get_server_routes(server_id='507f...')
route = servers.add_server_route(
    server_id='507f...',
    network='192.168.1.0/24',
    comment='Internal network',
    nat=True,
    nat_interface='eth0'
)
servers.delete_server_route(server_id='507f...', route_network='192.168.1.0-24')

# Host management
hosts = servers.get_server_hosts(server_id='507f...')
servers.attach_host(server_id='507f...', host_id='507f...')
servers.detach_host(server_id='507f...', host_id='507f...')

# Bandwidth statistics
bandwidth = servers.get_server_bandwidth(server_id='507f...', period='1d')

# Server output
output = servers.get_server_output(server_id='507f...')
servers.clear_server_output(server_id='507f...')
```

### Administrators

```python
from python_scripts import administrators

# List administrators
admins = administrators.list_administrators()

# Create administrator
admin = administrators.create_administrator(
    username='newadmin',
    password='secure_password',
    auth_api=True,
    super_user=False
)

# Update administrator
admin = administrators.update_administrator(
    admin_id='507f...',
    password='new_password',
    auth_api=True
)

# Delete administrator
administrators.delete_administrator(admin_id='507f...')

# Get audit log
logs = administrators.get_administrator_audit_log(admin_id='507f...')
```

### Settings

```python
from python_scripts import settings

# Get settings
current_settings = settings.get_settings()

# Update settings
updated_settings = settings.update_settings(
    theme='dark',
    email_from='vpn@example.com',
    sso=['google'],
    dns_servers=['8.8.8.8']
)

# Get available zones (AWS)
zones = settings.get_available_zones()
```

### Keys (VPN Configuration Downloads)

```python
from python_scripts import keys

# Download user keys in different formats
keys.download_user_keys_tar(
    org_id='507f...',
    user_id='507f...',
    save_path='/path/to/user_keys.tar'
)

keys.download_user_keys_zip(
    org_id='507f...',
    user_id='507f...',
    save_path='/path/to/user_keys.zip'
)

keys.download_user_keys_onc(
    org_id='507f...',
    user_id='507f...',
    save_path='/path/to/user_keys.onc'
)

# Get key URLs
key_urls = keys.get_user_key_urls(org_id='507f...', user_id='507f...')

# Download specific server key
keys.download_user_server_key(
    org_id='507f...',
    user_id='507f...',
    server_id='507f...',
    save_path='/path/to/server.key'
)
```

### Status & Monitoring

```python
from python_scripts import status, logs

# Get server status
server_status = status.get_status()
print(f"Version: {server_status['version']}")
print(f"Uptime: {server_status['uptime']}")

# Health check
status.ping()  # Returns {} if healthy

# Get events
events = status.get_events()
events_from_cursor = status.get_events(cursor='12345')

# Get logs
log_entries = logs.get_logs()
detailed_logs = logs.get_log_entries()
```

### Devices

```python
from python_scripts import devices

# Get unregistered devices
unregistered = devices.get_unregistered_devices()
for device in unregistered:
    print(f"Device: {device['name']} - {device['platform']}")

# Register device
devices.register_device(
    org_id='507f...',
    user_id='507f...',
    device_id='device123'
)

# Unregister device
devices.unregister_device(
    org_id='507f...',
    user_id='507f...',
    device_id='device123'
)
```

### Subscription

```python
from python_scripts import subscription

# Get subscription
sub = subscription.get_subscription()
print(f"Plan: {sub['plan']}")
print(f"Active: {sub['active']}")

# Activate subscription
subscription.activate_subscription(license_key='YOUR_LICENSE_KEY')

# Update subscription
subscription.update_subscription(license_key='NEW_LICENSE_KEY')

# Remove subscription
subscription.delete_subscription()
```

## Integration with Odoo

### Example: Odoo Model Integration

```python
from odoo import models, fields, api
from python_scripts import organizations, users, servers

class VpnUser(models.Model):
    _name = 'vpn.user'
    _description = 'VPN User'

    name = fields.Char('Name', required=True)
    email = fields.Char('Email', required=True)
    vpn_user_id = fields.Char('Pritunl User ID', readonly=True)
    org_id = fields.Char('Organization ID', required=True)
    groups = fields.Char('VPN Groups')
    disabled = fields.Boolean('Disabled', default=False)

    @api.model
    def create(self, vals):
        # Create record in Odoo
        record = super(VpnUser, self).create(vals)

        # Create user in Pritunl
        try:
            pritunl_user = users.create_user(
                org_id=record.org_id,
                name=record.name,
                email=record.email,
                groups=record.groups.split(',') if record.groups else [],
                disabled=record.disabled
            )

            # Store Pritunl user ID
            record.vpn_user_id = pritunl_user['id']

        except Exception as e:
            raise UserError(f"Failed to create VPN user: {str(e)}")

        return record

    def write(self, vals):
        # Update record in Odoo
        result = super(VpnUser, self).write(vals)

        # Update user in Pritunl if VPN-related fields changed
        if any(field in vals for field in ['name', 'email', 'groups', 'disabled']):
            try:
                users.update_user(
                    org_id=self.org_id,
                    user_id=self.vpn_user_id,
                    name=vals.get('name', self.name),
                    email=vals.get('email', self.email),
                    groups=vals.get('groups', self.groups).split(',') if vals.get('groups') else [],
                    disabled=vals.get('disabled', self.disabled)
                )
            except Exception as e:
                raise UserError(f"Failed to update VPN user: {str(e)}")

        return result

    def unlink(self):
        # Delete user from Pritunl
        for record in self:
            try:
                if record.vpn_user_id:
                    users.delete_user(
                        org_id=record.org_id,
                        user_id=record.vpn_user_id
                    )
            except Exception as e:
                raise UserError(f"Failed to delete VPN user: {str(e)}")

        # Delete record from Odoo
        return super(VpnUser, self).unlink()

    def action_download_vpn_keys(self):
        """Download VPN keys for this user"""
        from python_scripts import keys
        import tempfile

        if not self.vpn_user_id:
            raise UserError("VPN user not created yet")

        # Download keys to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        keys.download_user_keys_zip(
            org_id=self.org_id,
            user_id=self.vpn_user_id,
            save_path=temp_file.name
        )

        # Return download action (implement file download in Odoo)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?file_path={temp_file.name}',
            'target': 'new',
        }
```

### Example: Server Management in Odoo

```python
from odoo import models, fields, api
from python_scripts import servers

class VpnServer(models.Model):
    _name = 'vpn.server'
    _description = 'VPN Server'

    name = fields.Char('Server Name', required=True)
    server_id = fields.Char('Pritunl Server ID', readonly=True)
    status = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Status', default='offline')
    network = fields.Char('Network', required=True, default='10.0.0.0/8')
    port = fields.Integer('Port', default=15500)
    max_clients = fields.Integer('Max Clients', default=2048)

    def action_start_server(self):
        """Start VPN server"""
        for record in self:
            if not record.server_id:
                raise UserError("Server not created in Pritunl yet")

            try:
                servers.start_server(server_id=record.server_id)
                record.status = 'online'
            except Exception as e:
                raise UserError(f"Failed to start server: {str(e)}")

    def action_stop_server(self):
        """Stop VPN server"""
        for record in self:
            if not record.server_id:
                raise UserError("Server not created in Pritunl yet")

            try:
                servers.stop_server(server_id=record.server_id)
                record.status = 'offline'
            except Exception as e:
                raise UserError(f"Failed to stop server: {str(e)}")

    def action_restart_server(self):
        """Restart VPN server"""
        for record in self:
            if not record.server_id:
                raise UserError("Server not created in Pritunl yet")

            try:
                servers.restart_server(server_id=record.server_id)
            except Exception as e:
                raise UserError(f"Failed to restart server: {str(e)}")
```

## Error Handling

All API functions raise `requests.exceptions.RequestException` on failure:

```python
from python_scripts import users
import requests

try:
    user = users.create_user(
        org_id='invalid_id',
        name='test',
        email='test@example.com'
    )
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Status Code: {e.response.status_code}")
    print(f"Response: {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## API Modules

| Module | Description |
|--------|-------------|
| `authentication.py` | Session-based login/logout |
| `administrators.py` | Administrator management |
| `organizations.py` | Organization CRUD operations |
| `users.py` | User management, OTP, devices |
| `servers.py` | VPN server management, routes, hosts |
| `hosts.py` | Host management |
| `settings.py` | Application settings |
| `keys.py` | VPN key downloads |
| `links.py` | Site-to-site VPN links |
| `devices.py` | Device registration |
| `sso.py` | Single Sign-On |
| `logs.py` | Log retrieval |
| `status.py` | Server status and events |
| `subscription.py` | License management |

## Configuration

Edit `config.py` to configure your Pritunl server:

```python
# Pritunl Server Configuration
BASE_URL = "https://vpn1.craftron.co:8447"
API_TOKEN = "your_api_token_here"
API_SECRET = "your_api_secret_here"

# Request Configuration
REQUEST_TIMEOUT = 30  # seconds
VERIFY_SSL = True  # Set to False for self-signed certificates
```

## Getting API Credentials

1. Login to Pritunl web interface
2. Navigate to **Administrators**
3. Select your admin user
4. Enable **API Authentication**
5. Copy the **Token** and **Secret**

## Requirements

- Python 3.7+
- requests library

## License

This SDK is provided as-is for use with Pritunl VPN Server.

## Support

For issues with Pritunl server, visit: https://github.com/pritunl/pritunl

For issues with this SDK, contact your development team.
