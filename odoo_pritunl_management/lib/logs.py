"""
Pritunl Logs API
Functions for retrieving application logs and entries.
"""

from typing import Dict, Any, List
from .auth import PritunlAuth


def get_logs(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get application logs.

    Returns:
        List of log dictionaries

    Example:
        >>> logs = get_logs()
        >>> for log in logs:
        ...     print(f"{log['timestamp']}: {log['message']}")
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/log')


def get_log_entries(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get log entries.

    Returns:
        List of log entry dictionaries

    Example:
        >>> entries = get_log_entries()
        >>> for entry in entries:
        ...     print(f"{entry['time']}: {entry['msg']}")
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/logs')
