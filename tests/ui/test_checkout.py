import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import settings

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.desktop
def test_e2e_checkout_flow_desktop(
    authenticated_inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage
):
    """
    [SMOKE][DESKTOP] End-to-end checkout flow from product selection to order confirmation.
    """
    # 1. Add item to cart
    authenticated_inventory_page.add_product_to_cart_by_name("Sauce Labs Fleece Jacket")
    assert authenticated_inventory_page.get_cart_badge_count() == 1
    
    # 2. View Cart
    authenticated_inventory_page.open_cart()
    assert cart_page.is_loaded()
    assert "Sauce Labs Fleece Jacket" in cart_page.get_cart_item_names()
    
    # 3. Checkout Step One
    cart_page.proceed_to_checkout()
    checkout_page.fill_customer_info(
        settings.CUSTOMER_FIRST_NAME,
        settings.CUSTOMER_LAST_NAME,
        settings.CUSTOMER_POSTAL_CODE,
    )
    
    # 4. Checkout Step Two (Overview)
    expect(checkout_page.finish_button).to_be_visible()
    assert "Total:" in checkout_page.get_total_text()
    
    # 5. Finish order
    checkout_page.finish_order()
    assert checkout_page.is_order_complete()

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.mobile
def test_e2e_checkout_flow_mobile(
    authenticated_inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage
):
    """
    [SMOKE][MOBILE] End-to-end checkout flow on mobile viewport.
    """
    # 1. Add item on mobile
    authenticated_inventory_page.add_product_to_cart_by_name("Sauce Labs Onesie")
    assert authenticated_inventory_page.get_cart_badge_count() == 1
    
    # 2. Open cart and proceed
    authenticated_inventory_page.open_cart()
    assert cart_page.is_loaded()
    assert "Sauce Labs Onesie" in cart_page.get_cart_item_names()
    
    cart_page.proceed_to_checkout()
    checkout_page.fill_customer_info("Mobile", "Shopper", "90210")
    
    # 3. Finish order
    checkout_page.finish_order()
    assert checkout_page.is_order_complete()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_checkout_validation_empty_fields_desktop(
    authenticated_inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage
):
    """
    [REGRESSION][DESKTOP] Verify form validation when required fields are missing on checkout.
    """
    authenticated_inventory_page.add_product_to_cart_by_name("Sauce Labs Bolt T-Shirt")
    authenticated_inventory_page.open_cart()
    cart_page.proceed_to_checkout()
    
    # Attempt submit without entering customer details
    checkout_page.continue_button.click()
    
    expect(checkout_page.error_message).to_be_visible()
    assert "Error: First Name is required" in checkout_page.get_error_message()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_cart_remove_item_regression(
    authenticated_inventory_page: InventoryPage,
    cart_page: CartPage
):
    """
    [REGRESSION][DESKTOP] Verify user can remove an item directly from the cart page.
    """
    authenticated_inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    authenticated_inventory_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
    
    authenticated_inventory_page.open_cart()
    assert cart_page.get_cart_item_count() == 2
    
    cart_page.remove_item_by_name("Sauce Labs Backpack")
    assert cart_page.get_cart_item_count() == 1
    assert "Sauce Labs Backpack" not in cart_page.get_cart_item_names()
    assert "Sauce Labs Bike Light" in cart_page.get_cart_item_names()
