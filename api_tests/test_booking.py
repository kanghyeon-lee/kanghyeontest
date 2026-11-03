from typing import Any, Dict, List, Tuple

import pytest
from jsonschema import FormatChecker, validate

from api.booking_client import BookingClient
from api.payloads import booking_payload
from api.schemas import BOOKING_SCHEMA, CREATE_BOOKING_RESPONSE_SCHEMA

Booking = Tuple[int, Dict[str, Any]]


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(booking_payload(), id="default"),
        pytest.param(booking_payload(totalprice=0, depositpaid=False), id="zero-price-no-deposit"),
        pytest.param(booking_payload(firstname="강현", lastname="이", additionalneeds="조식 포함"), id="korean-text"),
        pytest.param(
            booking_payload(bookingdates={"checkin": "2027-02-28", "checkout": "2027-03-01"}, additionalneeds=""),
            id="month-boundary-empty-needs",
        ),
    ],
)
def test_create_booking_returns_created_values(
    client: BookingClient, created_booking_ids: List[int], payload: Dict[str, Any]
):
    response = client.create(payload)

    assert response.status_code == 200, response.text
    body = response.json()
    created_booking_ids.append(body["bookingid"])
    validate(body, CREATE_BOOKING_RESPONSE_SCHEMA, format_checker=FormatChecker())
    assert body["booking"] == payload


def test_get_booking_matches_created_values(client: BookingClient, booking: Booking):
    booking_id, payload = booking

    response = client.get(booking_id)

    assert response.status_code == 200
    body = response.json()
    validate(body, BOOKING_SCHEMA, format_checker=FormatChecker())
    assert body == payload


@pytest.mark.parametrize("booking_id", [999_999_999, 0, -1], ids=["huge-id", "zero", "negative"])
def test_get_nonexistent_booking_returns_404(client: BookingClient, booking_id: int):
    assert client.get(booking_id).status_code == 404


@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "invalid-token"])
@pytest.mark.parametrize("method", ["update", "partial_update"])
def test_update_without_valid_token_is_rejected(
    client: BookingClient, booking: Booking, method: str, token: Any
):
    booking_id, payload = booking
    change = booking_payload(firstname="Hacker", totalprice=1)

    response = getattr(client, method)(booking_id, change, token=token)

    assert response.status_code in (401, 403), response.text
    assert client.get(booking_id).json() == payload


@pytest.mark.parametrize(
    "new_values",
    [
        pytest.param(
            booking_payload(
                firstname="James", lastname="Kim", totalprice=999, depositpaid=False,
                bookingdates={"checkin": "2027-01-10", "checkout": "2027-01-15"}, additionalneeds="Late checkout",
            ),
            id="all-fields-changed",
        ),
        pytest.param(booking_payload(additionalneeds="Dinner"), id="one-field-changed"),
    ],
)
def test_update_booking_is_applied(client: BookingClient, token: str, booking: Booking, new_values: Dict[str, Any]):
    booking_id, _ = booking

    response = client.update(booking_id, new_values, token=token)

    assert response.status_code == 200, response.text
    assert response.json() == new_values
    assert client.get(booking_id).json() == new_values


@pytest.mark.parametrize(
    "fields",
    [
        pytest.param({"firstname": "Partial"}, id="firstname"),
        pytest.param({"totalprice": 500, "depositpaid": False}, id="price-and-deposit"),
        pytest.param({"bookingdates": {"checkin": "2027-05-01", "checkout": "2027-05-05"}}, id="bookingdates"),
    ],
)
def test_partial_update_changes_only_given_fields(
    client: BookingClient, token: str, booking: Booking, fields: Dict[str, Any]
):
    booking_id, payload = booking
    expected = {**payload, **fields}

    response = client.partial_update(booking_id, fields, token=token)

    assert response.status_code == 200, response.text
    assert response.json() == expected
    assert client.get(booking_id).json() == expected


def test_deleted_booking_returns_404(client: BookingClient, token: str, booking: Booking):
    booking_id, _ = booking

    response = client.delete(booking_id, token=token)

    assert response.ok, f"{response.status_code} {response.text}"
    assert client.get(booking_id).status_code == 404
