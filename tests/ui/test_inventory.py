import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.desktop
def test_inventory_items_displayed_desktop(authenticated_inventory_page: InventoryPage):
    """
    [SMOKE][DESKTOP] Verify products catalog loads on desktop and has items.
    """
    page = authenticated_inventory_page
    assert page.get_product_count() == 6
    product_names = page.get_all_product_names()
    assert "Sauce Labs Backpack" in product_names
    assert "Sauce Labs Bike Light" in product_names

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_sort_products_price_low_to_high_desktop(authenticated_inventory_page: InventoryPage):
    """
    [REGRESSION][DESKTOP] Verify sorting products by price low to high.
    """
    page = authenticated_inventory_page
    page.sort_by("lohi")
    
    prices = page.get_all_product_prices()
    assert prices == sorted(prices), f"Prices not sorted low to high: {prices}"

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_sort_products_name_z_to_a_desktop(authenticated_inventory_page: InventoryPage):
    """
    [REGRESSION][DESKTOP] Verify sorting products by name Z to A.
    """
    page = authenticated_inventory_page
    page.sort_by("za")
    
    names = page.get_all_product_names()
    assert names == sorted(names, reverse=True), f"Names not sorted Z to A: {names}"

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.mobile
def test_mobile_inventory_add_to_cart(authenticated_inventory_page: InventoryPage):
    """
    [SMOKE][MOBILE] Verify adding product to cart updates badge count on mobile.
    """
    page = authenticated_inventory_page
    assert page.get_cart_badge_count() == 0
    
    page.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert page.get_cart_badge_count() == 1
    
    page.add_product_to_cart_by_name("Sauce Labs Bike Light")
    assert page.get_cart_badge_count() == 2

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.desktop
def test_add_and_remove_item_desktop(authenticated_inventory_page: InventoryPage):
    """
    [REGRESSION][DESKTOP] Verify adding and then removing item resets cart badge count.
    """
    page = authenticated_inventory_page
    target_item = "Sauce Labs Backpack"
    
    page.add_product_to_cart_by_name(target_item)
    assert page.get_cart_badge_count() == 1
    
    page.remove_product_by_name(target_item)
    assert page.get_cart_badge_count() == 0
