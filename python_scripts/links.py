"""
Pritunl Links API
Functions for managing Pritunl Links (site-to-site VPN).
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


# ==================== LINKS ====================

def list_links(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get all Pritunl Links."""
    if client is None:
        client = PritunlAuth()
    return client.get('/link')


def create_link(
    name: str,
    type: str = 'direct',
    status: str = 'online',
    timeout: int = 30,
    mtu: int = 1500,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Create a new Pritunl Link."""
    if client is None:
        client = PritunlAuth()

    data = {
        'name': name,
        'type': type,
        'status': status,
        'timeout': timeout,
        'mtu': mtu
    }
    return client.post('/link', data=data)


def update_link(link_id: str, name: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Update a link."""
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.put(f'/link/{link_id}', data=data)


def delete_link(link_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Delete a link."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/link/{link_id}')


# ==================== LINK LOCATIONS ====================

def get_link_locations(link_id: str, client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """Get locations for a link."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/link/{link_id}/location')


def create_link_location(
    link_id: str,
    name: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Create a link location."""
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.post(f'/link/{link_id}/location', data=data)


def update_link_location(
    link_id: str,
    location_id: str,
    name: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Update a link location."""
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.put(f'/link/{link_id}/location/{location_id}', data=data)


def delete_link_location(
    link_id: str,
    location_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Delete a link location."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/link/{link_id}/location/{location_id}')


# ==================== LINK ROUTES ====================

def add_link_route(
    link_id: str,
    location_id: str,
    network: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Add a route to link location."""
    if client is None:
        client = PritunlAuth()

    data = {'network': network}
    return client.post(f'/link/{link_id}/location/{location_id}/route', data=data)


def delete_link_route(
    link_id: str,
    location_id: str,
    network: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Delete a route from link location. Network should use dash (e.g., '192.168.10.0-24')."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/link/{link_id}/location/{location_id}/route/{network}')


# ==================== LINK HOSTS ====================

def add_link_host(
    link_id: str,
    location_id: str,
    name: str,
    timeout: int = 30,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Add a host to link location."""
    if client is None:
        client = PritunlAuth()

    data = {
        'name': name,
        'timeout': timeout
    }
    return client.put(f'/link/{link_id}/location/{location_id}/host', data=data)


def get_link_host_uri(
    link_id: str,
    location_id: str,
    host_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Get link host URI."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/link/{link_id}/location/{location_id}/host/{host_id}/uri')


def get_link_host_config(
    link_id: str,
    location_id: str,
    host_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Get link host configuration."""
    if client is None:
        client = PritunlAuth()
    return client.get(f'/link/{link_id}/location/{location_id}/host/{host_id}/conf')


def update_link_host(
    link_id: str,
    location_id: str,
    host_id: str,
    name: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Update a link host."""
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.put(f'/link/{link_id}/location/{location_id}/host/{host_id}', data=data)


def delete_link_host(
    link_id: str,
    location_id: str,
    host_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """Delete a link host."""
    if client is None:
        client = PritunlAuth()
    return client.delete(f'/link/{link_id}/location/{location_id}/host/{host_id}')


# ==================== LINK STATE ====================

def update_link_state(status: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """Update link state (online/offline)."""
    if client is None:
        client = PritunlAuth()

    data = {'status': status}
    return client.put('/link/state', data=data)


def delete_link_state(client: PritunlAuth = None) -> Dict[str, Any]:
    """Delete link state."""
    if client is None:
        client = PritunlAuth()
    return client.delete('/link/state')
