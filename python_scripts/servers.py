"""
Pritunl Servers API
Functions for managing VPN servers, routes, hosts, and operations.
"""

from typing import Dict, Any, List, Optional
from .auth import PritunlAuth


# ==================== SERVER CRUD ====================

def list_servers(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get all VPN servers.

    Args:
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of server dictionaries

    Example:
        >>> servers = list_servers()
        >>> for server in servers:
        ...     print(server['name'], server['status'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get('/server')


def get_server(server_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Get server details by ID.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Server dictionary

    Example:
        >>> server = get_server('507f1f77bcf86cd799439011')
        >>> print(server['name'], server['port'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}')


def create_server(
    name: str,
    network: str,
    port: int = 15500,
    protocol: str = 'udp',
    dh_param_bits: int = 2048,
    groups: Optional[List[str]] = None,
    network_mode: str = 'tunnel',
    network_start: Optional[str] = None,
    network_end: Optional[str] = None,
    restrict_routes: bool = True,
    bind_address: Optional[str] = None,
    ipv6: bool = False,
    ipv6_firewall: bool = True,
    inter_client: bool = True,
    ping_interval: int = 10,
    ping_timeout: int = 60,
    link_ping_interval: int = 1,
    link_ping_timeout: int = 5,
    allowed_devices: Optional[str] = None,
    max_clients: int = 2048,
    max_devices: int = 1,
    replica_count: int = 1,
    dns_servers: Optional[List[str]] = None,
    search_domain: Optional[str] = None,
    otp_auth: bool = False,
    cipher: str = 'aes128',
    hash: str = 'sha1',
    multi_device: bool = False,
    dns_mapping: Optional[str] = None,
    debug: bool = False,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Create a new VPN server.

    Args:
        name: Server name
        network: Network address (e.g., '10.0.0.0/8')
        port: Server port
        protocol: Protocol (udp, tcp, udp6, tcp6)
        dh_param_bits: DH parameter bits (1536, 2048, 3072, 4096)
        groups: Server groups
        network_mode: Network mode (tunnel, bridge)
        network_start: Start IP address
        network_end: End IP address
        restrict_routes: Restrict routes to VPN
        bind_address: Bind address
        ipv6: Enable IPv6
        ipv6_firewall: Enable IPv6 firewall
        inter_client: Allow inter-client communication
        ping_interval: Ping interval in seconds
        ping_timeout: Ping timeout in seconds
        link_ping_interval: Link ping interval
        link_ping_timeout: Link ping timeout
        allowed_devices: Allowed devices (desktop, mobile)
        max_clients: Maximum number of clients
        max_devices: Maximum devices per user
        replica_count: Number of replicas
        dns_servers: DNS servers list
        search_domain: DNS search domain
        otp_auth: Require OTP authentication
        cipher: Encryption cipher
        hash: Hash algorithm
        multi_device: Allow multiple devices per user
        dns_mapping: DNS mapping
        debug: Enable debug mode
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Created server dictionary

    Example:
        >>> server = create_server(
        ...     name='Production VPN',
        ...     network='10.0.0.0/8',
        ...     port=15500,
        ...     dns_servers=['8.8.8.8', '8.8.4.4']
        ... )
        >>> print(f"Created server: {server['id']}")
    """
    if client is None:
        client = PritunlAuth()

    data = {
        'name': name,
        'network': network,
        'port': port,
        'protocol': protocol,
        'dh_param_bits': dh_param_bits,
        'network_mode': network_mode,
        'restrict_routes': restrict_routes,
        'ipv6': ipv6,
        'ipv6_firewall': ipv6_firewall,
        'inter_client': inter_client,
        'ping_interval': ping_interval,
        'ping_timeout': ping_timeout,
        'link_ping_interval': link_ping_interval,
        'link_ping_timeout': link_ping_timeout,
        'max_clients': max_clients,
        'max_devices': max_devices,
        'replica_count': replica_count,
        'otp_auth': otp_auth,
        'cipher': cipher,
        'hash': hash,
        'multi_device': multi_device,
        'debug': debug
    }

    if groups is not None:
        data['groups'] = groups
    if network_start is not None:
        data['network_start'] = network_start
    if network_end is not None:
        data['network_end'] = network_end
    if bind_address is not None:
        data['bind_address'] = bind_address
    if allowed_devices is not None:
        data['allowed_devices'] = allowed_devices
    if dns_servers is not None:
        data['dns_servers'] = dns_servers
    if search_domain is not None:
        data['search_domain'] = search_domain
    if dns_mapping is not None:
        data['dns_mapping'] = dns_mapping

    return client.post('/server', data=data)


def update_server(
    server_id: str,
    name: Optional[str] = None,
    network: Optional[str] = None,
    port: Optional[int] = None,
    protocol: Optional[str] = None,
    dh_param_bits: Optional[int] = None,
    groups: Optional[List[str]] = None,
    network_mode: Optional[str] = None,
    network_start: Optional[str] = None,
    network_end: Optional[str] = None,
    restrict_routes: Optional[bool] = None,
    bind_address: Optional[str] = None,
    ipv6: Optional[bool] = None,
    ipv6_firewall: Optional[bool] = None,
    inter_client: Optional[bool] = None,
    ping_interval: Optional[int] = None,
    ping_timeout: Optional[int] = None,
    link_ping_interval: Optional[int] = None,
    link_ping_timeout: Optional[int] = None,
    allowed_devices: Optional[str] = None,
    max_clients: Optional[int] = None,
    max_devices: Optional[int] = None,
    replica_count: Optional[int] = None,
    dns_servers: Optional[List[str]] = None,
    search_domain: Optional[str] = None,
    otp_auth: Optional[bool] = None,
    cipher: Optional[str] = None,
    hash: Optional[str] = None,
    multi_device: Optional[bool] = None,
    dns_mapping: Optional[str] = None,
    debug: Optional[bool] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Update a server.

    Args:
        server_id: Server ID
        name: Server name
        network: Network address
        port: Server port
        protocol: Protocol
        dh_param_bits: DH parameter bits
        groups: Server groups
        network_mode: Network mode
        network_start: Start IP address
        network_end: End IP address
        restrict_routes: Restrict routes
        bind_address: Bind address
        ipv6: Enable IPv6
        ipv6_firewall: Enable IPv6 firewall
        inter_client: Allow inter-client communication
        ping_interval: Ping interval
        ping_timeout: Ping timeout
        link_ping_interval: Link ping interval
        link_ping_timeout: Link ping timeout
        allowed_devices: Allowed devices
        max_clients: Maximum clients
        max_devices: Maximum devices per user
        replica_count: Replica count
        dns_servers: DNS servers
        search_domain: DNS search domain
        otp_auth: Require OTP
        cipher: Encryption cipher
        hash: Hash algorithm
        multi_device: Allow multiple devices
        dns_mapping: DNS mapping
        debug: Debug mode
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Updated server dictionary

    Example:
        >>> server = update_server(
        ...     server_id='507f1f77bcf86cd799439011',
        ...     name='Updated Server Name',
        ...     max_clients=4096
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {}

    if name is not None:
        data['name'] = name
    if network is not None:
        data['network'] = network
    if port is not None:
        data['port'] = port
    if protocol is not None:
        data['protocol'] = protocol
    if dh_param_bits is not None:
        data['dh_param_bits'] = dh_param_bits
    if groups is not None:
        data['groups'] = groups
    if network_mode is not None:
        data['network_mode'] = network_mode
    if network_start is not None:
        data['network_start'] = network_start
    if network_end is not None:
        data['network_end'] = network_end
    if restrict_routes is not None:
        data['restrict_routes'] = restrict_routes
    if bind_address is not None:
        data['bind_address'] = bind_address
    if ipv6 is not None:
        data['ipv6'] = ipv6
    if ipv6_firewall is not None:
        data['ipv6_firewall'] = ipv6_firewall
    if inter_client is not None:
        data['inter_client'] = inter_client
    if ping_interval is not None:
        data['ping_interval'] = ping_interval
    if ping_timeout is not None:
        data['ping_timeout'] = ping_timeout
    if link_ping_interval is not None:
        data['link_ping_interval'] = link_ping_interval
    if link_ping_timeout is not None:
        data['link_ping_timeout'] = link_ping_timeout
    if allowed_devices is not None:
        data['allowed_devices'] = allowed_devices
    if max_clients is not None:
        data['max_clients'] = max_clients
    if max_devices is not None:
        data['max_devices'] = max_devices
    if replica_count is not None:
        data['replica_count'] = replica_count
    if dns_servers is not None:
        data['dns_servers'] = dns_servers
    if search_domain is not None:
        data['search_domain'] = search_domain
    if otp_auth is not None:
        data['otp_auth'] = otp_auth
    if cipher is not None:
        data['cipher'] = cipher
    if hash is not None:
        data['hash'] = hash
    if multi_device is not None:
        data['multi_device'] = multi_device
    if dns_mapping is not None:
        data['dns_mapping'] = dns_mapping
    if debug is not None:
        data['debug'] = debug

    return client.put(f'/server/{server_id}', data=data)


def delete_server(server_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Delete a server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_server('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}')


# ==================== SERVER OPERATIONS ====================

def start_server(server_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Start a VPN server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> start_server('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/operation/start')


def stop_server(server_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Stop a VPN server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> stop_server('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/operation/stop')


def restart_server(server_id: str, client: PritunlAuth = None) -> Dict[str, Any]:
    """
    Restart a VPN server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> restart_server('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/operation/restart')


# ==================== SERVER ORGANIZATIONS ====================

def get_server_organizations(
    server_id: str,
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Get organizations attached to a server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of organization dictionaries

    Example:
        >>> orgs = get_server_organizations('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/organization')


def attach_organization(
    server_id: str,
    org_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Attach an organization to a server.

    Args:
        server_id: Server ID
        org_id: Organization ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> attach_organization('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/organization/{org_id}')


def detach_organization(
    server_id: str,
    org_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Detach an organization from a server.

    Args:
        server_id: Server ID
        org_id: Organization ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> detach_organization('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/organization/{org_id}')


# ==================== SERVER ROUTES ====================

def get_server_routes(
    server_id: str,
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Get routes for a server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of route dictionaries

    Example:
        >>> routes = get_server_routes('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/route')


def add_server_route(
    server_id: str,
    network: str,
    comment: Optional[str] = None,
    nat: bool = True,
    nat_interface: Optional[str] = None,
    nat_netmap: Optional[str] = None,
    advertise: bool = False,
    net_gateway: bool = False,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Add a route to a server.

    Args:
        server_id: Server ID
        network: Network CIDR (e.g., '192.168.1.0/24')
        comment: Route comment
        nat: Enable NAT
        nat_interface: NAT interface
        nat_netmap: NAT network mapping
        advertise: Advertise route
        net_gateway: Use net gateway
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Created route dictionary

    Example:
        >>> route = add_server_route(
        ...     server_id='507f1f77bcf86cd799439011',
        ...     network='192.168.1.0/24',
        ...     comment='Internal network',
        ...     nat=True,
        ...     nat_interface='eth0'
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {
        'network': network,
        'nat': nat,
        'advertise': advertise,
        'net_gateway': net_gateway
    }

    if comment is not None:
        data['comment'] = comment
    if nat_interface is not None:
        data['nat_interface'] = nat_interface
    if nat_netmap is not None:
        data['nat_netmap'] = nat_netmap

    return client.post(f'/server/{server_id}/route', data=data)


def add_multiple_routes(
    server_id: str,
    routes: List[Dict[str, Any]],
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Add multiple routes to a server.

    Args:
        server_id: Server ID
        routes: List of route dictionaries with 'network' and other optional fields
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of created route dictionaries

    Example:
        >>> routes = add_multiple_routes(
        ...     server_id='507f1f77bcf86cd799439011',
        ...     routes=[
        ...         {'network': '192.168.1.0/24'},
        ...         {'network': '192.168.2.0/24'}
        ...     ]
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {'routes': routes}
    return client.post(f'/server/{server_id}/routes', data=data)


def update_server_route(
    server_id: str,
    route_network: str,
    network: Optional[str] = None,
    comment: Optional[str] = None,
    nat: Optional[bool] = None,
    nat_interface: Optional[str] = None,
    nat_netmap: Optional[str] = None,
    advertise: Optional[bool] = None,
    net_gateway: Optional[bool] = None,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Update a server route.

    Note: route_network should use dash instead of slash (e.g., '192.168.1.0-24')

    Args:
        server_id: Server ID
        route_network: Current route network with dash (e.g., '192.168.1.0-24')
        network: New network CIDR
        comment: Route comment
        nat: Enable NAT
        nat_interface: NAT interface
        nat_netmap: NAT network mapping
        advertise: Advertise route
        net_gateway: Use net gateway
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Updated route dictionary

    Example:
        >>> route = update_server_route(
        ...     server_id='507f1f77bcf86cd799439011',
        ...     route_network='192.168.1.0-24',
        ...     comment='Updated comment'
        ... )
    """
    if client is None:
        client = PritunlAuth()

    data = {}

    if network is not None:
        data['network'] = network
    if comment is not None:
        data['comment'] = comment
    if nat is not None:
        data['nat'] = nat
    if nat_interface is not None:
        data['nat_interface'] = nat_interface
    if nat_netmap is not None:
        data['nat_netmap'] = nat_netmap
    if advertise is not None:
        data['advertise'] = advertise
    if net_gateway is not None:
        data['net_gateway'] = net_gateway

    return client.put(f'/server/{server_id}/route/{route_network}', data=data)


def delete_server_route(
    server_id: str,
    route_network: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Delete a server route.

    Note: route_network should use dash instead of slash (e.g., '192.168.1.0-24')

    Args:
        server_id: Server ID
        route_network: Route network with dash (e.g., '192.168.1.0-24')
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_server_route('507f1f77bcf86cd799439011', '192.168.1.0-24')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/route/{route_network}')


# ==================== SERVER HOSTS ====================

def get_server_hosts(
    server_id: str,
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Get hosts attached to a server.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of host dictionaries

    Example:
        >>> hosts = get_server_hosts('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/host')


def attach_host(
    server_id: str,
    host_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Attach a host to a server.

    Args:
        server_id: Server ID
        host_id: Host ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> attach_host('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/host/{host_id}')


def detach_host(
    server_id: str,
    host_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Detach a host from a server.

    Args:
        server_id: Server ID
        host_id: Host ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> detach_host('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/host/{host_id}')


# ==================== SERVER LINKS ====================

def get_server_links(
    server_id: str,
    client: PritunlAuth = None
) -> List[Dict[str, Any]]:
    """
    Get server links.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of link dictionaries

    Example:
        >>> links = get_server_links('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/link')


def create_server_link(
    server_id: str,
    link_server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Create a link between servers.

    Args:
        server_id: Server ID
        link_server_id: Link server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Created link dictionary

    Example:
        >>> link = create_server_link('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.put(f'/server/{server_id}/link/{link_server_id}')


def delete_server_link(
    server_id: str,
    link_server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Delete a server link.

    Args:
        server_id: Server ID
        link_server_id: Link server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> delete_server_link('507f1f77bcf86cd799439011', '507f191e810c19729de860ea')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/link/{link_server_id}')


# ==================== SERVER OUTPUT ====================

def get_server_output(
    server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Get server output logs.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Dictionary with server output

    Example:
        >>> output = get_server_output('507f1f77bcf86cd799439011')
        >>> print(output['output'])
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/output')


def clear_server_output(
    server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Clear server output.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> clear_server_output('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/output')


def get_server_link_output(
    server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Get server link output.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Dictionary with link output

    Example:
        >>> output = get_server_link_output('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/link_output')


def clear_server_link_output(
    server_id: str,
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Clear server link output.

    Args:
        server_id: Server ID
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Empty dictionary on success

    Example:
        >>> clear_server_link_output('507f1f77bcf86cd799439011')
    """
    if client is None:
        client = PritunlAuth()

    return client.delete(f'/server/{server_id}/link_output')


# ==================== SERVER BANDWIDTH ====================

def get_server_bandwidth(
    server_id: str,
    period: str = '1m',
    client: PritunlAuth = None
) -> Dict[str, Any]:
    """
    Get server bandwidth statistics.

    Args:
        server_id: Server ID
        period: Time period ('1m', '5m', '30m', '2h', '1d')
        client: PritunlAuth instance (creates new one if None)

    Returns:
        Dictionary with bandwidth data

    Example:
        >>> bandwidth = get_server_bandwidth('507f1f77bcf86cd799439011', period='1d')
    """
    if client is None:
        client = PritunlAuth()

    return client.get(f'/server/{server_id}/bandwidth/{period}')


# ==================== SERVER VPCs ====================

def get_server_vpcs(client: PritunlAuth = None) -> List[Dict[str, Any]]:
    """
    Get available VPC networks (AWS).

    Args:
        client: PritunlAuth instance (creates new one if None)

    Returns:
        List of VPC dictionaries

    Example:
        >>> vpcs = get_server_vpcs()
    """
    if client is None:
        client = PritunlAuth()

    return client.get('/server/vpcs')
