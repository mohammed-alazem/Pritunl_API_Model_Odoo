"""
Pritunl Settings API
Functions for managing application settings.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


def get_settings(client: PritunlAuth = None) -> Dict[str, Any]:
    """Get all application settings."""
    if client is None:
        client = PritunlAuth()
    return client.get('/settings')


def update_settings(
    server_cert: Optional[str] = None,
    server_key: Optional[str] = None,
    acme_domain: Optional[str] = None,
    auditing: Optional[str] = None,
    monitoring: Optional[str] = None,
    influxdb_uri: Optional[str] = None,
    email_from: Optional[str] = None,
    email_server: Optional[str] = None,
    email_username: Optional[str] = None,
    email_password: Optional[str] = None,
    sso: Optional[List[str]] = None,
    sso_match: Optional[List[str]] = None,
    sso_azure_directory_id: Optional[str] = None,
    sso_azure_app_id: Optional[str] = None,
    sso_azure_app_secret: Optional[str] = None,
    sso_google_key: Optional[str] = None,
    sso_google_email: Optional[str] = None,
    sso_org: Optional[str] = None,
    theme: Optional[str] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Update application settings.

    Example:
        >>> settings = update_settings(
        ...     theme='dark',
        ...     email_from='vpn@example.com',
        ...     sso=['google']
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {}
    if server_cert is not None:
        data['server_cert'] = server_cert
    if server_key is not None:
        data['server_key'] = server_key
    if acme_domain is not None:
        data['acme_domain'] = acme_domain
    if auditing is not None:
        data['auditing'] = auditing
    if monitoring is not None:
        data['monitoring'] = monitoring
    if influxdb_uri is not None:
        data['influxdb_uri'] = influxdb_uri
    if email_from is not None:
        data['email_from'] = email_from
    if email_server is not None:
        data['email_server'] = email_server
    if email_username is not None:
        data['email_username'] = email_username
    if email_password is not None:
        data['email_password'] = email_password
    if sso is not None:
        data['sso'] = sso
    if sso_match is not None:
        data['sso_match'] = sso_match
    if sso_azure_directory_id is not None:
        data['sso_azure_directory_id'] = sso_azure_directory_id
    if sso_azure_app_id is not None:
        data['sso_azure_app_id'] = sso_azure_app_id
    if sso_azure_app_secret is not None:
        data['sso_azure_app_secret'] = sso_azure_app_secret
    if sso_google_key is not None:
        data['sso_google_key'] = sso_google_key
    if sso_google_email is not None:
        data['sso_google_email'] = sso_google_email
    if sso_org is not None:
        data['sso_org'] = sso_org
    if theme is not None:
        data['theme'] = theme

    return client.put('/settings', data=data)


def get_available_zones(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get available AWS zones."""
    if client is None:
        client = PritunlAuth()
    return client.get('/settings/zones')
