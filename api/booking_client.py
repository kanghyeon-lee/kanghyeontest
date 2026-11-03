import os
from typing import Any, Dict, Optional

import requests

DEFAULT_BASE_URL = "https://restful-booker.herokuapp.com"
DEFAULT_TIMEOUT = 15  # seconds


class BookingClient:
    """restful-booker API 클라이언트. 모든 메서드는 검증 없이 requests.Response를 그대로 돌려준다."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT):
        self.base_url = (base_url or os.getenv("API_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def _request(self, method: str, path: str, token: Optional[str] = None, **kwargs: Any) -> requests.Response:
        headers = kwargs.pop("headers", {})
        if token is not None:
            headers["Cookie"] = f"token={token}"
        return self.session.request(
            method, f"{self.base_url}{path}", headers=headers, timeout=self.timeout, **kwargs
        )

    def auth(self, username: str, password: str) -> requests.Response:
        return self._request("POST", "/auth", json={"username": username, "password": password})

    def create(self, booking: Dict[str, Any]) -> requests.Response:
        return self._request("POST", "/booking", json=booking)

    def get(self, booking_id: int) -> requests.Response:
        return self._request("GET", f"/booking/{booking_id}")

    def update(self, booking_id: int, booking: Dict[str, Any], token: Optional[str] = None) -> requests.Response:
        return self._request("PUT", f"/booking/{booking_id}", token=token, json=booking)

    def partial_update(
        self, booking_id: int, fields: Dict[str, Any], token: Optional[str] = None
    ) -> requests.Response:
        return self._request("PATCH", f"/booking/{booking_id}", token=token, json=fields)

    def delete(self, booking_id: int, token: Optional[str] = None) -> requests.Response:
        return self._request("DELETE", f"/booking/{booking_id}", token=token)

    def close(self) -> None:
        self.session.close()
