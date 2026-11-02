from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

PRODUCT = "Sauce Labs Backpack"


def test_checkout_completes_order(logged_in: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    logged_in.add_to_cart(PRODUCT)
    logged_in.go_to_cart()

    cart_page.expect_loaded()
    cart_page.expect_contains(PRODUCT)
    cart_page.checkout()

    checkout_page.fill_information("Kanghyeon", "Test", "12345")
    checkout_page.finish()
    checkout_page.expect_complete()
