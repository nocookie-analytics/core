from typing import Dict
from unittest.mock import patch
from starlette.testclient import TestClient

from app.core.config import settings


def test_get_portal_url_no_auth(client: TestClient) -> None:
    resp = client.get(f"{settings.API_V1_STR}/billing/portal")
    assert resp.status_code == 401


def test_get_portal_url(client: TestClient, normal_user_token_headers: Dict) -> None:
    portal_url = "https://example.com"
    with patch(
        "app.api.api_v1.endpoints.billing.get_portal_session_url",
        return_value=portal_url,
    ):
        resp = client.get(
            f"{settings.API_V1_STR}/billing/portal", headers=normal_user_token_headers
        )
        assert resp.status_code == 200
        assert resp.json()["url"] == portal_url
