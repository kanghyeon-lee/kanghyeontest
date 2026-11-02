import re

from playwright.sync_api import Page, expect


class InventoryPage:
    URL_PATTERN = re.compile(r".*/inventory\.html$")

    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.inventory_list = page.get_by_test_id("inventory-list")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    def expect_loaded(self):
        expect(self.page).to_have_url(self.URL_PATTERN)
        expect(self.title).to_have_text("Products")
        expect(self.inventory_list).to_be_visible()

    def add_to_cart(self, product_name: str):
        item = self.page.get_by_test_id("inventory-item").filter(has_text=product_name)
        item.get_by_role("button", name="Add to cart").click()

    def expect_cart_count(self, count: int):
        expect(self.cart_badge).to_have_text(str(count))

    def go_to_cart(self):
        self.cart_link.click()
