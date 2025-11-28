"""
Pritunl Devices API
Functions for managing device registration and approval.
"""

from typing import Dict, Any, List
from .auth import PritunlAuth


def get_unregistered_devices(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get list of unregistered devices awaiting approval.

    Example:
        >>> devices = get_unregistered_devices()
        >>> for device in devices:
        ...     print(f"{device['name']} - {device['platform']}")
    """
    if client is None:
        client = PritunlAuth()
    return client.get('/device/unregistered')


def register_device(
    org_id: str,
    user_id: str,
    device_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Register/approve a device.

    Args:
        org_id: Organization ID
        user_id: User ID
        device_id: Device ID

    Example:
        >>> register_device('507f1f77bcf86cd799439011', '507f191e810c19729de860ea', 'device123')
    """
    if client is None:
        client = PritunlAuth()
    return client.put(f'/device/register/{org_id}/{user_id}/{device_id}')


def unregister_device(
    org_id: str,
    user_id: str,
    device_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Unregister/reject a device.

    Args:
        org_id: Organization ID
        user_id: User ID
        device_id: Device ID

    Example:
        >>> unregister_device('507f1f77bcf86cd799439011', '507f191e810c19729de860ea', 'device123')
    """
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/device/register/{org_id}/{user_id}/{device_id}')
