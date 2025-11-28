"""
Pritunl Administrators API
Functions for managing system administrators.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


def list_administrators(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get all administrators."""
    if client is None:
        client = PritunlAuth()
    return client.get('/admin')


def get_administrator(admin_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Get administrator details by ID."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/admin/{admin_id}')


def create_administrator(
    username: str,
    password: str,
    auth_api: bool = True,
    super_user: bool = False,
    disabled: bool = False,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Create a new administrator.

    Example:
        >>> admin = create_administrator(
        ...     username='newadmin',
        ...     password='secure_pass',
        ...     auth_api=True
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {
        'username': username,
        'password': password,
        'auth_api': auth_api,
        'super_user': super_user,
        'disabled': disabled
    }
    return client.post('/admin', data=data)


def update_administrator(
    admin_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    auth_api: Optional[bool] = None,
    super_user: Optional[bool] = None,
    disabled: Optional[bool] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Update an administrator."""
    if client is None:
        client = PritunlAuth()

    data = {}
    if username is not None:
        data['username'] = username
    if password is not None:
        data['password'] = password
    if auth_api is not None:
        data['auth_api'] = auth_api
    if super_user is not None:
        data['super_user'] = super_user
    if disabled is not None:
        data['disabled'] = disabled

    return client.put(f'/admin/{admin_id}', data=data)


def delete_administrator(admin_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Delete an administrator."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/admin/{admin_id}')


def get_administrator_audit_log(admin_id: str, client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get audit log for an administrator."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/admin/{admin_id}/audit')
