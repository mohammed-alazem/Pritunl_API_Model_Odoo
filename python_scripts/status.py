"""
Pritunl Status & Events API
Functions for monitoring server status and events.
"""

from typing import Dict, Any, Optional
from .auth import PritunlAuth


def get_status(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get server status and statistics.

    Returns:
        Dictionary with server status, version, uptime, etc.

    Example:
        >>> status = get_status()
        >>> print(f"Server version: {status['version']}")
        >>> print(f"User count: {status['user_count']}")
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/status')


def get_events(cursor: Optional[str] = None, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get server events (Server-Sent Events stream).

    Args:
        cursor: Optional cursor position to get events from

    Returns:
        Dictionary with events data

    Example:
        >>> events = get_events()
        >>> # For polling from specific cursor:
        >>> events = get_events(cursor='12345')
    """
    if client is None:
        client = PritunlAuth()

    if cursor:
        return client.get(f'/event/{cursor}')
    return client.get('/event')


def ping(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Empty dictionary if server is healthy

    Example:
        >>> ping()
        >>> # Returns {} if server is up
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/ping', authenticated=False)


def check(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Health check endpoint (alternative).

    Returns:
        Empty dictionary if server is healthy

    Example:
        >>> check()
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/check', authenticated=False)
