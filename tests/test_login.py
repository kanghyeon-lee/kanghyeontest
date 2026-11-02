import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_standard_user_login_shows_inventory(login_page: LoginPage, inventory_page: InventoryPage):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.expect_loaded()


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param(
            "standard_user", "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="wrong-password",
        ),
        pytest.param(
            "", "secret_sauce",
            "Epic sadface: Username is required",
            id="empty-username",
        ),
        pytest.param(
            "locked_out_user", "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
            id="locked-out-user",
        ),
    ],
)
def test_login_failure_shows_error(login_page: LoginPage, username: str, password: str, expected_error: str):
    login_page.open()
    login_page.login(username, password)
    login_page.expect_error(expected_error)
