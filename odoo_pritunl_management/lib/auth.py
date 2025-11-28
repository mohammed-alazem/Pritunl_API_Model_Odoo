"""
Pritunl API Authentication Module
Handles HMAC-SHA256 authentication for Pritunl API requests.
"""

import time
import hmac
import hashlib
import base64
import secrets
import requests
from typing import Dict, Any, Optional
from . import config


class PritunlAuth:
    """
    Handles authentication and HTTP requests to Pritunl API with HMAC-SHA256 signatures.
    """

    def __init__(
        self,
        base_url: str = None,
        api_token: str = None,
        api_secret: str = None,
        verify_ssl: bool = None,
        timeout: int = None
    ):
        """
        Initialize Pritunl API client.

        Args:
            base_url: Pritunl server URL (defaults to config.BASE_URL)
            api_token: API token (defaults to config.API_TOKEN)
            api_secret: API secret (defaults to config.API_SECRET)
            verify_ssl: Whether to verify SSL certificates (defaults to config.VERIFY_SSL)
            timeout: Request timeout in seconds (defaults to config.REQUEST_TIMEOUT)
        """
        self.base_url = (base_url or config.BASE_URL).rstrip('/')
        self.api_token = api_token or config.API_TOKEN
        self.api_secret = api_secret or config.API_SECRET
        self.verify_ssl = verify_ssl if verify_ssl is not None else config.VERIFY_SSL
        self.timeout = timeout or config.REQUEST_TIMEOUT

        if not self.api_token or not self.api_secret:
            raise ValueError("API token and secret must be provided")

    def _generate_nonce(self) -> str:
        """Generate a secure random nonce (32 hex characters)."""
        return secrets.token_hex(16)

    def _generate_signature(
        self,
        method: str,
        path: str,
        timestamp: str,
        nonce: str
    ) -> str:
        """
        Generate HMAC-SHA256 signature for API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            timestamp: Unix timestamp as string
            nonce: Random nonce string

        Returns:
            Base64-encoded HMAC-SHA256 signature
        """
        # Build auth string: token&timestamp&nonce&METHOD&path
        auth_string = '&'.join([
            self.api_token,
            timestamp,
            nonce,
            method.upper(),
            path
        ])

        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            auth_string.encode('utf-8'),
            hashlib.sha256
        ).digest()

        # Return base64-encoded signature
        return base64.b64encode(signature).decode('utf-8')

    def _get_auth_headers(self, method: str, path: str) -> Dict[str, str]:
        """
        Generate authentication headers for API request.

        Args:
            method: HTTP method
            path: API endpoint path

        Returns:
            Dictionary of authentication headers
        """
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        signature = self._generate_signature(method, path, timestamp, nonce)

        return {
            'Auth-Token': self.api_token,
            'Auth-Timestamp': timestamp,
            'Auth-Nonce': nonce,
            'Auth-Signature': signature,
            'Content-Type': 'application/json'
        }

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = True
    ) -> requests.Response:
        """
        Make an authenticated HTTP request to Pritunl API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/server')
            data: Request body data (for POST/PUT)
            params: URL query parameters
            authenticated: Whether to include authentication headers

        Returns:
            requests.Response object

        Raises:
            requests.exceptions.RequestException: On request failure
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint

        url = f"{self.base_url}{endpoint}"

        # Prepare headers
        headers = {}
        if authenticated:
            headers = self._get_auth_headers(method, endpoint)
        else:
            headers = {'Content-Type': 'application/json'}

        # Make request
        response = requests.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            headers=headers,
            verify=self.verify_ssl,
            timeout=self.timeout
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        return response

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = True
    ) -> Dict[str, Any]:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint
            params: URL query parameters
            authenticated: Whether to include authentication headers

        Returns:
            Parsed JSON response
        """
        response = self.request('GET', endpoint, params=params, authenticated=authenticated)
        return response.json() if response.content else {}

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        authenticated: bool = True
    ) -> Dict[str, Any]:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            data: Request body data
            authenticated: Whether to include authentication headers

        Returns:
            Parsed JSON response
        """
        response = self.request('POST', endpoint, data=data, authenticated=authenticated)
        return response.json() if response.content else {}

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        authenticated: bool = True
    ) -> Dict[str, Any]:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            data: Request body data
            authenticated: Whether to include authentication headers

        Returns:
            Parsed JSON response
        """
        response = self.request('PUT', endpoint, data=data, authenticated=authenticated)
        return response.json() if response.content else {}

    def delete(
        self,
        endpoint: str,
        authenticated: bool = True
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            authenticated: Whether to include authentication headers

        Returns:
            Parsed JSON response
        """
        response = self.request('DELETE', endpoint, authenticated=authenticated)
        return response.json() if response.content else {}
