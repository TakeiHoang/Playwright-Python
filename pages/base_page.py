import os
from typing import Optional
from playwright.sync_api import Page, Locator, Response

class BasePage:
    """Base class for all Page Object Models."""
    
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> Optional[Response]:
        """Navigate to a specified URL."""
        return self.page.goto(url, wait_until="domcontentloaded")

    def wait_for_url(self, url_or_pattern: str, timeout: Optional[int] = None) -> None:
        """Wait until page URL matches pattern or string."""
        self.page.wait_for_url(url_or_pattern, timeout=timeout)

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return current URL."""
        return self.page.url

    def take_screenshot(self, filename: str) -> bytes:
        """Save a screenshot into artifacts/screenshots directory."""
        os.makedirs("artifacts/screenshots", exist_ok=True)
        filepath = os.path.join("artifacts", "screenshots", filename)
        return self.page.screenshot(path=filepath, full_page=True)
