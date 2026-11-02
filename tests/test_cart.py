from pages.inventory_page import InventoryPage


def test_add_one_product_updates_cart_badge(logged_in: InventoryPage):
    logged_in.add_to_cart("Sauce Labs Backpack")
    logged_in.expect_cart_count(1)
