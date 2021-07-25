from app.core.products import Plan
from typing import Dict
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient

from app.core.config import settings
from app.tests.utils.domain import create_random_domain
from app.tests.utils.user import create_random_user, user_authentication_headers
from app.tests.utils.utils import random_lower_string


def test_get_portal_url_no_auth(client: TestClient) -> None:
    resp = client.get(f"{settings.API_V1_STR}/billing/portal/")
    assert resp.status_code == 401


def test_get_portal_url(client: TestClient, normal_user_token_headers: Dict) -> None:
    portal_url = "https://example.com"
    with patch(
        "app.api.api_v1.endpoints.billing.get_portal_session_url",
        return_value=portal_url,
    ):
        resp = client.get(
            f"{settings.API_V1_STR}/billing/portal/", headers=normal_user_token_headers
        )
        assert resp.status_code == 200
        assert resp.json()["url"] == portal_url


class TestSubscribe:
    def test_subscribe_no_auth(
        self,
        client: TestClient,
    ) -> None:
        resp = client.get(f"{settings.API_V1_STR}/billing/portal/")
        assert resp.status_code == 401

    def test_subscribe_wrong_plan(
        self, client: TestClient, normal_user_token_headers: Dict
    ):
        resp = client.get(
            f"{settings.API_V1_STR}/billing/subscribe",
            headers=normal_user_token_headers,
            params={"plan": Plan.NO_PLAN.value},
        )
        assert resp.status_code == 400, resp.content
        assert "looking for is not here" in resp.json()["detail"]

    def test_subscribe_no_stripe_customer(
        self, client: TestClient, normal_user_token_headers: Dict
    ):
        with patch("app.api.api_v1.endpoints.billing.create_stripe_customer_for_user"):
            resp = client.get(
                f"{settings.API_V1_STR}/billing/subscribe",
                headers=normal_user_token_headers,
                params={"plan": Plan.LITE.value},
            )
            assert resp.status_code == 500, resp.content

    def test_subscribe_customer_hsa_existing_subscription(
        self, client: TestClient, db: Session
    ):
        password = random_lower_string()
        user = create_random_user(db, password=password)
        headers = user_authentication_headers(
            client=client, email=user.email, password=password
        )
        user.stripe_customer_id = "cust_6414515"
        db.commit()
        with patch.multiple(
            "app.api.api_v1.endpoints.billing",
            create_stripe_customer_for_user=MagicMock(),
            get_stripe_subscriptions_for_user=MagicMock(return_value=[1]),
        ):
            resp = client.get(
                f"{settings.API_V1_STR}/billing/subscribe",
                headers=headers,
                params={"plan": Plan.LITE.value},
            )
            assert resp.status_code == 400, resp.content
            assert "already exists" in resp.json()["detail"]

    def test_subscribe_success(self, client: TestClient, db: Session):
        password = random_lower_string()
        user = create_random_user(db, password=password)
        headers = user_authentication_headers(
            client=client, email=user.email, password=password
        )
        user.stripe_customer_id = "cust_123456"
        db.commit()
        with patch.multiple(
            "app.api.api_v1.endpoints.billing",
            create_stripe_customer_for_user=MagicMock(),
            get_stripe_subscriptions_for_user=MagicMock(),
            create_checkout_session=MagicMock(return_value="https://example.com"),
        ):
            resp = client.get(
                f"{settings.API_V1_STR}/billing/subscribe",
                headers=headers,
                params={"plan": Plan.LITE.value},
            )
            assert resp.status_code == 200, resp.content
            assert resp.json()["url"] == "https://example.com"
