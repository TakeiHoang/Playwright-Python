import os
import pytest
from typing import Generator
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, APIRequestContext, sync_playwright

from config.settings import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from api.users_client import UsersApiClient
from api.auth_client import AuthApiClient

def pytest_addoption(parser):
    """Register custom command-line flags."""
    parser.addoption(
        "--ui-base-url",
        action="store",
        default=settings.UI_BASE_URL,
        help="Base URL for UI web testing",
    )
    parser.addoption(
        "--api-base-url",
        action="store",
        default=settings.API_BASE_URL,
        help="Base URL for API testing",
    )

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Shared Playwright manager."""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser_instance(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Shared Chromium browser instance launched in headless mode."""
    browser = playwright_instance.chromium.launch(
        headless=settings.HEADLESS,
        slow_mo=settings.SLOW_MO,
    )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def desktop_context(browser_instance: Browser) -> Generator[BrowserContext, None, None]:
    """Browser context configured for desktop viewport."""
    context = browser_instance.new_context(
        viewport=settings.DESKTOP_VIEWPORT,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def mobile_context(playwright_instance: Playwright, browser_instance: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """Browser context configured for mobile emulation."""
    device_opt = request.config.getoption("--device", default=None)
    device_name = device_opt if device_opt else settings.MOBILE_DEVICE_NAME
    
    device_config = playwright_instance.devices.get(device_name, playwright_instance.devices.get("Pixel 5", {}))
    context = browser_instance.new_context(**device_config)
    yield context
    context.close()

@pytest.fixture(scope="function")
def app_page(request: pytest.FixtureRequest, desktop_context: BrowserContext, mobile_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Intelligent Page fixture:
    - If test is marked with @pytest.mark.mobile, provisions a mobile context/page.
    - If test is marked with @pytest.mark.desktop, provisions a desktop context/page.
    - If --device=<name> is passed via CLI, respects mobile device emulation.
    """
    cli_device = request.config.getoption("--device", default=None)
    has_mobile_mark = request.node.get_closest_marker("mobile") is not None
    has_desktop_mark = request.node.get_closest_marker("desktop") is not None

    if has_mobile_mark or (cli_device and not has_desktop_mark):
        page = mobile_context.new_page()
    else:
        page = desktop_context.new_page()

    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    yield page
    
    # Teardown: Capture screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("artifacts/failures", exist_ok=True)
        screenshot_path = os.path.join("artifacts", "failures", f"{request.node.name}.png")
        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except Exception:
            pass
    page.close()

# ---------------------------------------------------------------------------
# Page Object Model Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def login_page(app_page: Page) -> LoginPage:
    """Fixture providing initialized LoginPage instance."""
    return LoginPage(app_page)

@pytest.fixture(scope="function")
def inventory_page(app_page: Page) -> InventoryPage:
    """Fixture providing initialized InventoryPage instance."""
    return InventoryPage(app_page)

@pytest.fixture(scope="function")
def cart_page(app_page: Page) -> CartPage:
    """Fixture providing initialized CartPage instance."""
    return CartPage(app_page)

@pytest.fixture(scope="function")
def checkout_page(app_page: Page) -> CheckoutPage:
    """Fixture providing initialized CheckoutPage instance."""
    return CheckoutPage(app_page)

@pytest.fixture(scope="function")
def authenticated_inventory_page(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """
    Fast-track fixture that authenticates with standard_user
    and returns ready-to-use InventoryPage.
    """
    login_page.load()
    login_page.login(settings.STANDARD_USER, settings.STANDARD_PASSWORD)
    assert inventory_page.is_loaded(), "Failed to reach inventory page after login"
    return inventory_page

# ---------------------------------------------------------------------------
# API Testing Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def api_request_context(playwright_instance: Playwright, request: pytest.FixtureRequest) -> Generator[APIRequestContext, None, None]:
    """Shared Playwright APIRequestContext fixture."""
    base_url = request.config.getoption("--api-base-url") or settings.API_BASE_URL
    context = playwright_instance.request.new_context(
        base_url=base_url,
        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    yield context
    context.dispose()

@pytest.fixture(scope="function")
def users_api(api_request_context: APIRequestContext, request: pytest.FixtureRequest) -> UsersApiClient:
    """Fixture providing UsersApiClient instance."""
    base_url = request.config.getoption("--api-base-url") or settings.API_BASE_URL
    return UsersApiClient(api_request_context, base_url)

@pytest.fixture(scope="function")
def auth_api(api_request_context: APIRequestContext, request: pytest.FixtureRequest) -> AuthApiClient:
    """Fixture providing AuthApiClient instance."""
    base_url = request.config.getoption("--api-base-url") or settings.API_BASE_URL
    return AuthApiClient(api_request_context, base_url)

# ---------------------------------------------------------------------------
# Pytest Hooks for Failure Diagnostics
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status for screenshot capture on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
