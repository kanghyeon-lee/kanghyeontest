from typing import Any, Dict, Iterator, List, Tuple

import pytest

from api.booking_client import BookingClient
from api.payloads import ADMIN_PASSWORD, ADMIN_USERNAME, booking_payload


@pytest.fixture(scope="session")
def client() -> Iterator[BookingClient]:
    c = BookingClient()
    yield c
    c.close()


@pytest.fixture(scope="session")
def token(client: BookingClient) -> str:
    response = client.auth(ADMIN_USERNAME, ADMIN_PASSWORD)
    assert response.status_code == 200, response.text
    return response.json()["token"]


@pytest.fixture
def booking(client: BookingClient, token: str) -> Iterator[Tuple[int, Dict[str, Any]]]:
    """테스트용 예약을 만들고 (bookingid, 생성 시 보낸 데이터)를 넘긴다. 테스트 후 삭제한다."""
    payload = booking_payload()
    response = client.create(payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]

    yield booking_id, payload

    # 테스트 안에서 이미 지웠을 수 있으므로 결과는 검사하지 않는다
    client.delete(booking_id, token=token)


@pytest.fixture
def created_booking_ids(client: BookingClient, token: str) -> Iterator[List[int]]:
    """테스트가 직접 생성한 예약 ID를 여기에 append하면 테스트 후 삭제한다."""
    ids: List[int] = []
    yield ids
    for booking_id in ids:
        client.delete(booking_id, token=token)
