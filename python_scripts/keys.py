"""
Pritunl Keys API
Functions for downloading VPN keys and configuration files.
"""

from typing import Optional
from .auth import PritunlAuth
import requests


def download_user_keys_tar(
    org_id: str,
    user_id: str,
    save_path: str,
    client: PritunlAuth = None
) -> None:
    """Download user keys as TAR archive."""
    if client is None:
        client = PritunlAuth()

    response = client.request('GET', f'/data/{org_id}/{user_id}.tar')
    with open(save_path, 'wb') as f:
        f.write(response.content)


def download_user_keys_zip(
    org_id: str,
    user_id: str,
    save_path: str,
    client: PritunlAuth = None
) -> None:
    """Download user keys as ZIP archive."""
    if client is None:
        client = PritunlAuth()

    response = client.request('GET', f'/data/{org_id}/{user_id}.zip')
    with open(save_path, 'wb') as f:
        f.write(response.content)


def download_user_keys_onc(
    org_id: str,
    user_id: str,
    save_path: str,
    client: PritunlAuth = None
) -> None:
    """Download user keys in ONC format for ChromeOS."""
    if client is None:
        client = PritunlAuth()

    response = client.request('GET', f'/data/{org_id}/{user_id}.onc')
    with open(save_path, 'wb') as f:
        f.write(response.content)


def get_user_key_urls(
    org_id: str,
    user_id: str,
    client: PritunlAuth = None
):
    """Get user key download URLs."""
    if client is None:
        client = PritunlAuth()

    return client.get(f'/data/{org_id}/{user_id}')


def download_user_server_key(
    org_id: str,
    user_id: str,
    server_id: str,
    save_path: str,
    client: PritunlAuth = None
) -> None:
    """Download specific server key for user."""
    if client is None:
        client = PritunlAuth()

    response = client.request('GET', f'/data/{org_id}/{user_id}/{server_id}.key')
    with open(save_path, 'wb') as f:
        f.write(response.content)
