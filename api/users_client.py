from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from api.base_api import BaseApiClient

class UsersApiClient(BaseApiClient):
    """API client for Users management endpoints."""
    
    USERS_ENDPOINT = "/api/users"

    def __init__(self, request_context: APIRequestContext, base_url: str):
        super().__init__(request_context, base_url)

    def get_users_list(self, page: int = 1) -> APIResponse:
        """Fetch paginated users list."""
        return self.get(self.USERS_ENDPOINT, params={"page": page})

    def get_user_by_id(self, user_id: int) -> APIResponse:
        """Fetch a specific user by ID."""
        return self.get(f"{self.USERS_ENDPOINT}/{user_id}")

    def create_user(self, name: str, job: str) -> APIResponse:
        """Create a new user with name and job."""
        payload = {"name": name, "job": job}
        return self.post(self.USERS_ENDPOINT, data=payload)

    def update_user(self, user_id: int, name: str, job: str) -> APIResponse:
        """Update an existing user via PUT."""
        payload = {"name": name, "job": job}
        return self.put(f"{self.USERS_ENDPOINT}/{user_id}", data=payload)

    def delete_user(self, user_id: int) -> APIResponse:
        """Delete an existing user via DELETE."""
        return self.delete(f"{self.USERS_ENDPOINT}/{user_id}")
