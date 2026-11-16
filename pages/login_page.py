from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from config.settings import settings

class LoginPage(BasePage):
    """Page Object Model for SauceDemo Login Page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator('[data-test="username"]')
        self.password_input: Locator = page.locator('[data-test="password"]')
        self.login_button: Locator = page.locator('[data-test="login-button"]')
        self.error_message: Locator = page.locator('[data-test="error"]')
        self.login_logo: Locator = page.locator(".login_logo")

    def load(self) -> None:
        """Navigate to SauceDemo login page."""
        self.navigate(settings.UI_BASE_URL)

    def login(self, username: str, password: str) -> None:
        """Fill in credentials and submit login form."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        """Return the error message text if visible."""
        return self.error_message.inner_text()

    def is_error_visible(self) -> bool:
        """Check if error message container is visible."""
        return self.error_message.is_visible()
