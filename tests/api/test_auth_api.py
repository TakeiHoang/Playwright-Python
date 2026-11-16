import pytest
from api.auth_client import AuthApiClient

@pytest.mark.api
@pytest.mark.smoke
def test_login_successful_smoke(auth_api: AuthApiClient):
    """
    [SMOKE][API] Verify valid credentials return 200 with an auth token.
    """
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = auth_api.login(payload)
    
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    body = response.json()
    assert "token" in body
    assert len(body["token"]) > 0

@pytest.mark.api
@pytest.mark.regression
def test_login_unsuccessful_missing_password_regression(auth_api: AuthApiClient):
    """
    [REGRESSION][API] Verify login without password returns HTTP 400 Bad Request.
    """
    payload = {
        "email": "peter@klaven"
    }
    response = auth_api.login(payload)
    
    assert response.status == 400
    body = response.json()
    assert body.get("error") == "Missing password"

@pytest.mark.api
@pytest.mark.regression
def test_register_unsuccessful_missing_password_regression(auth_api: AuthApiClient):
    """
    [REGRESSION][API] Verify user registration without password returns HTTP 400.
    """
    payload = {
        "email": "sydney@fife"
    }
    response = auth_api.register(payload)
    
    assert response.status == 400
    body = response.json()
    assert body.get("error") == "Missing password"
