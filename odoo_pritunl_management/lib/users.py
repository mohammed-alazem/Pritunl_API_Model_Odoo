"""
Pritunl Users API
Functions for managing VPN users within organizations.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


def list_users(org_id: str, client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get all users in an organization.

    Args:
        org_id: Organization ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of user dictionaries

    Example:
        >>> users = list_users('507f1f77bcf86cd799439011')
        >>> for user in users:
        ...     print(user['name'], user['email'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/user/{org_id}')


def get_user(
    org_id: str,
    user_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Get user details by ID.

    Args:
        org_id: Organization ID
        user_id: User ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        User dictionary

    Example:
        >>> user = get_user('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
        >>> print(user['name'], user['email'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/user/{org_id}/{user_id}')


def create_user(
    org_id: str,
    name: str,
    email: Optional[str] = None,
    pin: Optional[str] = None,
    disabled: bool = False,
    groups: Optional[List[str]] = None,
    bypass_secondary: bool = False,
    client_to_client: bool = False,
    dns_servers: Optional[List[str]] = None,
    dns_suffix: Optional[str] = None,
    port_forwarding: Optional[List[Dict[str, Any]]] = None,
    network_links: Optional[List[str]] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Create a new user in an organization.

    Args:
        org_id: Organization ID
        name: Username
        email: User email address
        pin: User PIN for additional authentication
        disabled: Whether user is disabled
        groups: List of group names
        bypass_secondary: Bypass secondary authentication
        client_to_client: Allow client-to-client communication
        dns_servers: Custom DNS servers for user
        dns_suffix: DNS search suffix
        port_forwarding: Port forwarding rules
        network_links: Network links
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Created user dictionary

    Example:
        >>> user = create_user(
        ...     org_id='507f1f77bcf86cd799439011',
        ...     name='john.doe',
        ...     email='john@example.com',
        ...     groups=['developers', 'vpn-users']
        ... )
        >>> print(f"Created user: {user['id']}")
    """
    if client is None:
        client = PritunlAuth()

    data = {
        'name': name,
        'disabled': disabled,
        'bypass_secondary': bypass_secondary,
        'client_to_client': client_to_client
    }

    if email is not None:
        data['email'] = email
    if pin is not None:
        data['pin'] = pin
    if groups is not None:
        data['groups'] = groups
    if dns_servers is not None:
        data['dns_servers'] = dns_servers
    if dns_suffix is not None:
        data['dns_suffix'] = dns_suffix
    if port_forwarding is not None:
        data['port_forwarding'] = port_forwarding
    if network_links is not None:
        data['network_links'] = network_links

    return client.post(f'/user/{org_id}', data=data)


def create_multiple_users(
    org_id: str,
    users: List[Dict[str, Any]],
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Create multiple users at once.

    Args:
        org_id: Organization ID
        users: List of user dictionaries with 'name' and optional 'email'
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of created user dictionaries

    Example:
        >>> users = create_multiple_users(
        ...     org_id='507f1f77bcf86cd799439011',
        ...     users=[
        ...         {'name': 'user1', 'email': 'user1@example.com'},
        ...         {'name': 'user2', 'email': 'user2@example.com'}
        ...     ]
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {'users': users}
    return client.post(f'/user/{org_id}/multi', data=data)


def update_user(
    org_id: str,
    user_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    pin: Optional[str] = None,
    disabled: Optional[bool] = None,
    groups: Optional[List[str]] = None,
    bypass_secondary: Optional[bool] = None,
    client_to_client: Optional[bool] = None,
    dns_servers: Optional[List[str]] = None,
    dns_suffix: Optional[str] = None,
    port_forwarding: Optional[List[Dict[str, Any]]] = None,
    network_links: Optional[List[str]] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Update a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        name: Username
        email: User email
        pin: User PIN
        disabled: Whether user is disabled
        groups: List of group names
        bypass_secondary: Bypass secondary authentication
        client_to_client: Allow client-to-client communication
        dns_servers: Custom DNS servers
        dns_suffix: DNS search suffix
        port_forwarding: Port forwarding rules
        network_links: Network links
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Updated user dictionary

    Example:
        >>> user = update_user(
        ...     org_id='507f1f77bcf86cd799439011',
        ...     user_id='507f191e810c19729de860ea',
        ...     email='newemail@example.com',
        ...     groups=['developers', 'admins']
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {}

    if name is not None:
        data['name'] = name
    if email is not None:
        data['email'] = email
    if pin is not None:
        data['pin'] = pin
    if disabled is not None:
        data['disabled'] = disabled
    if groups is not None:
        data['groups'] = groups
    if bypass_secondary is not None:
        data['bypass_secondary'] = bypass_secondary
    if client_to_client is not None:
        data['client_to_client'] = client_to_client
    if dns_servers is not None:
        data['dns_servers'] = dns_servers
    if dns_suffix is not None:
        data['dns_suffix'] = dns_suffix
    if port_forwarding is not None:
        data['port_forwarding'] = port_forwarding
    if network_links is not None:
        data['network_links'] = network_links

    return client.put(f'/user/{org_id}/{user_id}', data=data)


def delete_user(
    org_id: str,
    user_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Delete a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_user('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/user/{org_id}/{user_id}')


def generate_otp_secret(
    org_id: str,
    user_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Generate a new OTP secret for a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Dictionary with new OTP secret and QR code URL

    Example:
        >>> otp = generate_otp_secret('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
        >>> print(f"OTP Secret: {otp['secret']}")
        >>> print(f"QR Code: {otp['otpauth_url']}")
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/user/{org_id}/{user_id}/otp_secret')


def get_user_audit_log(
    org_id: str,
    user_id: str,
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Get audit log for a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of audit log entries

    Example:
        >>> logs = get_user_audit_log('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
        >>> for log in logs:
        ...     print(log['timestamp'], log['message'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/user/{org_id}/{user_id}/audit')


def approve_device(
    org_id: str,
    user_id: str,
    device_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Approve a device for a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        device_id: Device ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> approve_device('507f1f77bcf86cd799439011', '507f191e810c19729de860ea', 'device123')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/user/{org_id}/{user_id}/device/{device_id}')


def delete_device(
    org_id: str,
    user_id: str,
    device_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Delete a device for a user.

    Args:
        org_id: Organization ID
        user_id: User ID
        device_id: Device ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_device('507f1f77bcf86cd799439011', '507f191e810c19729de860ea', 'device123')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/user/{org_id}/{user_id}/device/{device_id}')


def find_user_by_name(
    org_id: str,
    name: str,
    client: PritunlAuth = None
) -> Optional[Dict[str, Any]]:
    """
    Find a user by name within an organization.

    Args:
        org_id: Organization ID
        name: Username to search for
        client: PritunlAuth instance (creates new one if None)

    Returns:
        User dictionary if found, None otherwise

    Example:
        >>> user = find_user_by_name('507f1f77bcf86cd799439011', 'john.doe')
        >>> if user:
        ...     print(f"Found: {user['id']}")
    """
    if client is None:
        client = PritunlAuth()

    users = list_users(org_id, client=client)
    for user in users:
        if user.get('name') == name:
            return user
    return None


def get_or_create_user(
    org_id: str,
    name: str,
    email: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Get an existing user by name, or create it if it doesn't exist.

    Args:
        org_id: Organization ID
        name: Username
        email: User email
        **kwargs: Additional arguments passed to create_user

    Returns:
        User dictionary

    Example:
        >>> user = get_or_create_user(
        ...     org_id='507f1f77bcf86cd799439011',
        ...     name='john.doe',
        ...     email='john@example.com'
        ... )
    """
    client = kwargs.pop('client', None)
    if client is None:
        client = PritunlAuth()

    # Try to find existing user
    user = find_user_by_name(org_id, name, client=client)
    if user:
        return user

    # Create new user
    return create_user(org_id=org_id, name=name, email=email, client=client, **kwargs)
