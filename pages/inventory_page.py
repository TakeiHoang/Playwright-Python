from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """Page Object Model for SauceDemo Inventory / Products Page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.title: Locator = page.locator(".title")
        self.inventory_container: Locator = page.locator(".inventory_list")
        self.inventory_items: Locator = page.locator(".inventory_item")
        self.item_names: Locator = page.locator(".inventory_item_name")
        self.item_prices: Locator = page.locator(".inventory_item_price")
        self.sort_select: Locator = page.locator('[data-test="product-sort-container"]')
        self.cart_badge: Locator = page.locator(".shopping_cart_badge")
        self.cart_link: Locator = page.locator(".shopping_cart_link")
        self.burger_menu_btn: Locator = page.locator("#react-burger-menu-btn")
        self.logout_link: Locator = page.locator("#logout_sidebar_link")
        self.close_menu_btn: Locator = page.locator("#react-burger-cross-btn")

    def is_loaded(self) -> bool:
        """Verify inventory page has loaded."""
        return self.title.is_visible() and self.title.inner_text().strip() == "Products"

    def get_product_count(self) -> int:
        """Return total number of visible products."""
        return self.inventory_items.count()

    def get_all_product_names(self) -> List[str]:
        """Return list of all product names displayed."""
        return self.item_names.all_inner_texts()

    def get_all_product_prices(self) -> List[float]:
        """Return list of all product prices as floats."""
        raw_prices = self.item_prices.all_inner_texts()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Find product card by name and click its 'Add to cart' button."""
        card = self.inventory_items.filter(has_text=product_name)
        card.locator("button").click()

    def remove_product_by_name(self, product_name: str) -> None:
        """Find product card by name and click its 'Remove' button."""
        card = self.inventory_items.filter(has_text=product_name)
        card.locator("button").click()

    def get_cart_badge_count(self) -> int:
        """Return numeric count from the cart badge or 0 if badge is not displayed."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text().strip())
        return 0

    def sort_by(self, option_value: str) -> None:
        """Sort products using select value ('az', 'za', 'lohi', 'hilo')."""
        self.sort_select.select_option(option_value)

    def open_cart(self) -> None:
        """Click cart icon to go to cart page."""
        self.cart_link.click()

    def open_burger_menu(self) -> None:
        """Open mobile/desktop drawer burger menu."""
        self.burger_menu_btn.click()
        self.logout_link.wait_for(state="visible")

    def logout(self) -> None:
        """Open menu and logout."""
        self.open_burger_menu()
        self.logout_link.click()
