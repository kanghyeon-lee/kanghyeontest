from typing import Any, Dict

# restful-booker 공개 문서에 명시된 관리자 계정
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


def booking_payload(**overrides: Any) -> Dict[str, Any]:
    """기본 예약 데이터. 필요한 필드만 덮어써서 쓴다."""
    payload: Dict[str, Any] = {
        "firstname": "Kanghyeon",
        "lastname": "Lee",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-03"},
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload
