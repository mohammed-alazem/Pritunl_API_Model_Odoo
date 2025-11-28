"""
Pritunl Subscription API
Functions for managing Pritunl subscription and licensing.
"""

from typing import Dict, Any
from .auth import PritunlAuth


def get_subscription(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get subscription information.

    Returns:
        Dictionary with subscription details

    Example:
        >>> subscription = get_subscription()
        >>> print(f"Plan: {subscription['plan']}")
        >>> print(f"Active: {subscription['active']}")
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/subscription')


def activate_subscription(license_key: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Activate subscription with license key.

    Args:
        license_key: Pritunl license key

    Returns:
        Dictionary with activation result

    Example:
        >>> result = activate_subscription('YOUR_LICENSE_KEY')
    """
    if client is None:
        client = PritunlAuth()

    data = {'license': license_key}
    return client.post('/subscription', data=data)


def update_subscription(license_key: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Update subscription with new license key.

    Args:
        license_key: New Pritunl license key

    Returns:
        Dictionary with update result

    Example:
        >>> result = update_subscription('NEW_LICENSE_KEY')
    """
    if client is None:
        client = PritunlAuth()

    data = {'license': license_key}
    return client.put('/subscription', data=data)


def delete_subscription(client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Remove subscription.

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_subscription()
    """
    if client is None:
        client = PritunlAuth()
    return client.delete('/subscription')
