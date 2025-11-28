"""
Pritunl SSO API
Functions for Single Sign-On authentication.
Note: These endpoints are typically used by the web interface, not for API automation.
"""

from typing import Dict, Any, Optional
from .auth import PritunlAuth


def sso_authenticate(
    username: str,
    password: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """SSO authentication endpoint."""
    if client is None:
        client = PritunlAuth()

    data = {
        'username': username,
        'password': password
    }
    return client.post('/sso/authenticate', data=data, authenticated=False)


def sso_request(client: PritunlAuth = None) -> Dict[str, Any]:
    """Initiate SSO request."""
    if client is None:
        client = PritunlAuth()
    return client.get('/sso/request', authenticated=False)


def sso_duo(
    username: str,
    factor: str = 'push',
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Duo Security SSO authentication."""
    if client is None:
        client = PritunlAuth()

    data = {
        'username': username,
        'factor': factor
    }
    return client.post('/sso/duo', data=data, authenticated=False)


def sso_yubico(
    username: str,
    yubico_key: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Yubico SSO authentication."""
    if client is None:
        client = PritunlAuth()

    data = {
        'username': username,
        'yubico_key': yubico_key
    }
    return client.post('/sso/yubico', data=data, authenticated=False)
