from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse

class BaseApiClient:
    """Base API client wrapping Playwright's APIRequestContext."""
    
    def __init__(self, request_context: APIRequestContext, base_url: str = ""):
        self.request = request_context
        self.base_url = base_url.rstrip("/")

    def _resolve_url(self, endpoint: str) -> str:
        """Combine base URL with endpoint if relative."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        clean_endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{clean_endpoint}" if self.base_url else endpoint

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Send a GET request."""
        url = self._resolve_url(endpoint)
        return self.request.get(url, params=params, headers=headers)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Send a POST request with JSON payload."""
        url = self._resolve_url(endpoint)
        return self.request.post(url, data=data, headers=headers)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Send a PUT request with JSON payload."""
        url = self._resolve_url(endpoint)
        return self.request.put(url, data=data, headers=headers)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Send a PATCH request with JSON payload."""
        url = self._resolve_url(endpoint)
        return self.request.patch(url, data=data, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Send a DELETE request."""
        url = self._resolve_url(endpoint)
        return self.request.delete(url, headers=headers)
