"""
Pritunl Hosts API
Functions for managing VPN hosts.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


def list_hosts(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get all hosts."""
    if client is None:
        client = PritunlAuth()
    return client.get('/host')


def get_host(host_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Get host details by ID."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/host/{host_id}')


def update_host(
    host_id: str,
    name: Optional[str] = None,
    public_address: Optional[str] = None,
    routed_subnet6: Optional[str] = None,
    link_address: Optional[str] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Update a host."""
    if client is None:
        client = PritunlAuth()

    data = {}
    if name is not None:
        data['name'] = name
    if public_address is not None:
        data['public_address'] = public_address
    if routed_subnet6 is not None:
        data['routed_subnet6'] = routed_subnet6
    if link_address is not None:
        data['link_address'] = link_address

    return client.put(f'/host/{host_id}', data=data)


def delete_host(host_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Delete a host."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/host/{host_id}')


def get_host_usage(
    host_id: str,
    period: str = '1m',
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Get host usage statistics.

    Args:
        host_id: Host ID
        period: Time period ('1m', '5m', '30m', '2h', '1d')
    """
    if client is None:
        client = PritunlAuth()
    return client.get(f'/host/{host_id}/usage/{period}')
