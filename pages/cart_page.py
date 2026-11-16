from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object Model for SauceDemo Shopping Cart Page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.title: Locator = page.locator(".title")
        self.cart_items: Locator = page.locator(".cart_item")
        self.item_names: Locator = page.locator(".inventory_item_name")
        self.checkout_button: Locator = page.locator('[data-test="checkout"]')
        self.continue_shopping_btn: Locator = page.locator('[data-test="continue-shopping"]')

    def is_loaded(self) -> bool:
        """Verify cart page has loaded."""
        return self.title.is_visible() and self.title.inner_text().strip() == "Your Cart"

    def get_cart_item_names(self) -> List[str]:
        """Return names of all items in cart."""
        return self.item_names.all_inner_texts()

    def get_cart_item_count(self) -> int:
        """Return number of items in cart."""
        return self.cart_items.count()

    def remove_item_by_name(self, product_name: str) -> None:
        """Remove item from cart by product name."""
        item = self.cart_items.filter(has_text=product_name)
        item.locator("button").click()

    def proceed_to_checkout(self) -> None:
        """Click checkout button to proceed to Step 1 checkout."""
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        """Click continue shopping button to return to inventory."""
        self.continue_shopping_btn.click()
