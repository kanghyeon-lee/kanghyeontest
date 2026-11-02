import re

from playwright.sync_api import Page, expect


class CartPage:
    URL_PATTERN = re.compile(r".*/cart\.html$")

    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def expect_loaded(self):
        expect(self.page).to_have_url(self.URL_PATTERN)

    def expect_contains(self, product_name: str):
        expect(self.items.filter(has_text=product_name)).to_have_count(1)

    def checkout(self):
        self.checkout_button.click()
