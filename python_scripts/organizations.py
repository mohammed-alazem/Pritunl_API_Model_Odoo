"""
Pritunl Organizations API
Functions for managing VPN organizations.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


def list_organizations(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get all organizations.

    Args:
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of organization dictionaries

    Example:
        >>> orgs = list_organizations()
        >>> for org in orgs:
        ...     print(org['name'], org['id'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get('/organization')


def get_organization(org_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get organization details by ID.

    Args:
        org_id: Organization ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Organization dictionary

    Example:
        >>> org = get_organization('507f1f77bcf86cd799439011')
        >>> print(org['name'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/organization/{org_id}')


def create_organization(name: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Create a new organization.

    Args:
        name: Organization name
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Created organization dictionary

    Example:
        >>> org = create_organization('Engineering Team')
        >>> print(f"Created organization: {org['id']}")
    """
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.post('/organization', data=data)


def update_organization(
    org_id: str,
    name: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Update an organization.

    Args:
        org_id: Organization ID
        name: New organization name
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Updated organization dictionary

    Example:
        >>> org = update_organization('507f1f77bcf86cd799439011', 'New Name')
    """
    if client is None:
        client = PritunlAuth()

    data = {'name': name}
    return client.put(f'/organization/{org_id}', data=data)


def delete_organization(org_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Delete an organization.

    Args:
        org_id: Organization ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_organization('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/organization/{org_id}')


def find_organization_by_name(name: str, client: PritunlAuth = None) -> Optional[Dict[str, Any]]:
    """
    Find an organization by name.

    Args:
        name: Organization name to search for
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Organization dictionary if found, None otherwise

    Example:
        >>> org = find_organization_by_name('Engineering Team')
        >>> if org:
        ...     print(f"Found: {org['id']}")
    """
    if client is None:
        client = PritunlAuth()

    orgs = list_organizations(client=client)
    for org in orgs:
        if org.get('name') == name:
            return org
    return None


def get_or_create_organization(name: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get an existing organization by name, or create it if it doesn't exist.

    Args:
        name: Organization name
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Organization dictionary

    Example:
        >>> org = get_or_create_organization('Sales Team')
        >>> print(f"Organization ID: {org['id']}")
    """
    if client is None:
        client = PritunlAuth()

    # Try to find existing organization
    org = find_organization_by_name(name, client=client)
    if org:
        return org

    # Create new organization
    return create_organization(name, client=client)
