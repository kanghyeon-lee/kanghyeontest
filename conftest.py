import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture(autouse=True, scope="session")
def _set_test_id_attribute(playwright):
    # saucedemo.com은 data-testid 대신 data-test 속성을 사용한다
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def logged_in(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """standard_user로 로그인해 상품 목록 페이지에 도착한 상태."""
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.expect_loaded()
    return inventory_page
