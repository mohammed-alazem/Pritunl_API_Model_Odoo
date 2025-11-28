"""
Pritunl Authentication API
Functions for session-based authentication.
"""

from typing import Dict, Any, Optional
from .auth import PritunlAuth


def login(
    username: str,
    password: str,
    otp_code: Optional[str] = None,
    yubico_key: Optional[str] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Create a new session (login).

    Args:
        username: Admin username
        password: Admin password
        otp_code: OTP code if enabled
        yubico_key: Yubico key if enabled

    Returns:
        Dictionary with authentication status and token

    Example:
        >>> result = login('admin', 'password123')
        >>> if result['authenticated']:
        ...     print('Login successful')
    """
    if client is None:
        client = PritunlAuth()

    data = {
        'username': username,
        'password': password
    }
    if otp_code:
        data['otp_code'] = otp_code
    if yubico_key:
        data['yubico_key'] = yubico_key

    return client.post('/auth/session', data=data, authenticated=False)


def logout(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Delete current session (logout).

    Returns:
        Dictionary with authentication status (should be False)

    Example:
        >>> logout()
    """
    if client is None:
        client = PritunlAuth()

    return client.delete('/auth/session', authenticated=False)


def get_state(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get current application state.

    Returns:
        Dictionary with server state, version, theme, etc.

    Example:
        >>> state = get_state()
        >>> print(f"Version: {state['version']}")
        >>> print(f"Theme: {state['theme']}")
    """
    if client is None:
        client = PritunlAuth()

    return client.get('/state')
