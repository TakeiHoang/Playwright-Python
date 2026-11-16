from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from api.base_api import BaseApiClient

class AuthApiClient(BaseApiClient):
    """API client for Authentication endpoints."""
    
    LOGIN_ENDPOINT = "/api/login"
    REGISTER_ENDPOINT = "/api/register"

    def __init__(self, request_context: APIRequestContext, base_url: str):
        super().__init__(request_context, base_url)

    def login(self, payload: Dict[str, Any]) -> APIResponse:
        """Authenticate user with login payload."""
        return self.post(self.LOGIN_ENDPOINT, data=payload)

    def register(self, payload: Dict[str, Any]) -> APIResponse:
        """Register user with payload."""
        return self.post(self.REGISTER_ENDPOINT, data=payload)
