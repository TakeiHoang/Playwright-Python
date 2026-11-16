from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Page Object Model for SauceDemo Multi-Step Checkout Flow."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Step One: Customer Information
        self.step_one_title: Locator = page.locator(".title")
        self.first_name_input: Locator = page.locator('[data-test="firstName"]')
        self.last_name_input: Locator = page.locator('[data-test="lastName"]')
        self.postal_code_input: Locator = page.locator('[data-test="postalCode"]')
        self.continue_button: Locator = page.locator('[data-test="continue"]')
        self.error_message: Locator = page.locator('[data-test="error"]')
        
        # Step Two: Overview & Summary
        self.subtotal_label: Locator = page.locator(".summary_subtotal_label")
        self.tax_label: Locator = page.locator(".summary_tax_label")
        self.total_label: Locator = page.locator(".summary_total_label")
        self.finish_button: Locator = page.locator('[data-test="finish"]')
        
        # Complete Order Page
        self.complete_header: Locator = page.locator(".complete-header")
        self.complete_text: Locator = page.locator(".complete-text")
        self.back_home_button: Locator = page.locator('[data-test="back-to-products"]')

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in checkout contact form and proceed."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def get_error_message(self) -> str:
        """Return error message text on step one validation failure."""
        return self.error_message.inner_text()

    def get_total_text(self) -> str:
        """Return total price label string (e.g. 'Total: $32.39')."""
        return self.total_label.inner_text()

    def finish_order(self) -> None:
        """Click Finish button to complete checkout."""
        self.finish_button.click()

    def is_order_complete(self) -> bool:
        """Verify order completion confirmation is visible."""
        return (
            self.complete_header.is_visible() 
            and "thank you for your order" in self.complete_header.inner_text().lower()
        )
