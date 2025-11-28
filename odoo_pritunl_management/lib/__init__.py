"""
Pritunl API Python SDK
Professional Python SDK for Pritunl VPN Server API

This package provides a complete Python interface to the Pritunl VPN Server API,
with HMAC-SHA256 authentication and comprehensive endpoint coverage.

Usage:
    from python_scripts import organizations, users, servers

    # List all organizations
    orgs = organizations.list_organizations()

    # Create a new user
    user = users.create_user(org_id="...", name="john.doe", email="john@example.com")

    # Start a VPN server
    servers.start_server(server_id="...")

"""

__version__ = "1.0.0"
__author__ = "Pritunl API SDK"
