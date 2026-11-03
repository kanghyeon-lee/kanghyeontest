import pytest

from api.booking_client import BookingClient
from api.payloads import ADMIN_PASSWORD, ADMIN_USERNAME


def test_auth_with_valid_credentials_returns_token(client: BookingClient):
    response = client.auth(ADMIN_USERNAME, ADMIN_PASSWORD)

    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str) and token


@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(ADMIN_USERNAME, "wrong_password", id="wrong-password"),
        pytest.param("unknown_user", ADMIN_PASSWORD, id="unknown-username"),
        pytest.param("", "", id="empty-credentials"),
    ],
)
def test_auth_with_invalid_credentials_returns_no_token(client: BookingClient, username: str, password: str):
    response = client.auth(username, password)

    body = response.json()
    assert "token" not in body
    assert body.get("reason") == "Bad credentials"
