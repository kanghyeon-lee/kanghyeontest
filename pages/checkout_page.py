from playwright.sync_api import Page, expect


class CheckoutPage:
    """checkout-step-one(정보 입력) → step-two(주문 확인) → complete 흐름."""

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_test_id("firstName")
        self.last_name_input = page.get_by_test_id("lastName")
        self.postal_code_input = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    def expect_complete(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")
