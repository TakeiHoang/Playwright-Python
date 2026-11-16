import pytest
from api.users_client import UsersApiClient

@pytest.mark.api
@pytest.mark.smoke
def test_get_users_list_smoke(users_api: UsersApiClient):
    """
    [SMOKE][API] Verify GET /api/users returns HTTP 200 with user list schema.
    """
    response = users_api.get_users_list(page=1)
    
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    body = response.json()
    assert body["page"] == 1
    assert "data" in body
    assert len(body["data"]) > 0
    
    first_user = body["data"][0]
    assert "id" in first_user
    assert "email" in first_user
    assert "first_name" in first_user
    assert "last_name" in first_user

@pytest.mark.api
@pytest.mark.smoke
def test_get_single_user_smoke(users_api: UsersApiClient):
    """
    [SMOKE][API] Verify GET /api/users/2 returns HTTP 200 with correct user profile.
    """
    response = users_api.get_user_by_id(2)
    
    assert response.status == 200
    body = response.json()
    assert body["data"]["id"] == 2
    assert body["data"]["email"] == "janet.weaver@reqres.in"

@pytest.mark.api
@pytest.mark.regression
def test_create_user_regression(users_api: UsersApiClient):
    """
    [REGRESSION][API] Verify POST /api/users creates a new user and returns HTTP 201.
    """
    payload_name = "Alice Test"
    payload_job = "QA Architect"
    
    response = users_api.create_user(name=payload_name, job=payload_job)
    
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    body = response.json()
    assert body["name"] == payload_name
    assert body["job"] == payload_job
    assert "id" in body
    assert "createdAt" in body

@pytest.mark.api
@pytest.mark.regression
def test_update_user_regression(users_api: UsersApiClient):
    """
    [REGRESSION][API] Verify PUT /api/users/2 updates user data and returns HTTP 200.
    """
    updated_name = "Janet Senior QA"
    updated_job = "Lead Engineer"
    
    response = users_api.update_user(user_id=2, name=updated_name, job=updated_job)
    
    assert response.status == 200
    body = response.json()
    assert body["name"] == updated_name
    assert body["job"] == updated_job
    assert "updatedAt" in body

@pytest.mark.api
@pytest.mark.regression
def test_delete_user_regression(users_api: UsersApiClient):
    """
    [REGRESSION][API] Verify DELETE /api/users/2 returns HTTP 204 No Content.
    """
    response = users_api.delete_user(user_id=2)
    assert response.status == 204

@pytest.mark.api
@pytest.mark.regression
def test_user_not_found_regression(users_api: UsersApiClient):
    """
    [REGRESSION][API] Verify GET /api/users/23 (non-existent) returns HTTP 404.
    """
    response = users_api.get_user_by_id(9999)
    assert response.status == 404
    assert response.json() == {}
