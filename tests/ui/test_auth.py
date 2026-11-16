import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import settings

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.desktop
def test_valid_login_desktop(login_page: LoginPage, inventory_page: InventoryPage):
    """
    [SMOKE][DESKTOP] Verify standard_user can log in successfully on desktop.
    """
    login_page.load()
    login_page.login(settings.STANDARD_USER, settings.STANDARD_PASSWORD)
    
    expect(inventory_page.title).to_be_visible()
    expect(inventory_page.title).to_have_text("Products")
    assert "/inventory.html" in inventory_page.get_current_url()

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.mobile
def test_valid_login_mobile(login_page: LoginPage, inventory_page: InventoryPage):
    """
    [SMOKE][MOBILE] Verify standard_user can log in successfully on mobile viewport.
    """
    login_page.load()
    login_page.login(settings.STANDARD_USER, settings.STANDARD_PASSWORD)
    
    expect(inventory_page.title).to_be_visible()
    expect(inventory_page.burger_menu_btn).to_be_visible()
    assert "/inventory.html" in inventory_page.get_current_url()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_locked_out_user_desktop(login_page: LoginPage):
    """
    [REGRESSION][DESKTOP] Verify locked_out_user sees error notice.
    """
    login_page.load()
    login_page.login(settings.LOCKED_OUT_USER, settings.STANDARD_PASSWORD)
    
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_invalid_password_desktop(login_page: LoginPage):
    """
    [REGRESSION][DESKTOP] Verify error message with invalid password.
    """
    login_page.load()
    login_page.login(settings.STANDARD_USER, "wrong_password_123")
    
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Username and password do not match any user in this service")

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_empty_credentials_desktop(login_page: LoginPage):
    """
    [REGRESSION][DESKTOP] Verify validation error when submitting blank credentials.
    """
    login_page.load()
    login_page.login_button.click()
    
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Epic sadface: Username is required")

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.mobile
def test_mobile_drawer_logout(login_page: LoginPage, inventory_page: InventoryPage):
    """
    [REGRESSION][MOBILE] Verify user can open mobile burger drawer menu and log out.
    """
    login_page.load()
    login_page.login(settings.STANDARD_USER, settings.STANDARD_PASSWORD)
    
    inventory_page.logout()
    expect(login_page.login_button).to_be_visible()
    assert inventory_page.get_current_url() == f"{settings.UI_BASE_URL}/"
