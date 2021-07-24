import pytest
from sqlalchemy.orm.session import Session
from starlette.requests import Request
import stripe

from app.core.config import settings
from app.core.products import Plan
from app.models.user import User
from app.tests.utils.user import create_random_user
from app.utils.stripe_helpers import (
    cancel_stripe_subscription,
    create_checkout_session,
    create_stripe_customer_for_user,
    get_portal_session,
    get_stripe_prices,
    get_stripe_subscriptions_for_user,
    get_user_from_stripe_customer_id,
)


@pytest.fixture(scope="class")
def user(db: Session) -> User:
    return create_random_user(db)


@pytest.mark.vcr()
class TestStripe:
    def test_stripe_api_key_is_test_mode(self):
        if settings.STRIPE_API_KEY:
            assert settings.STRIPE_API_KEY.startswith("sk_test_")

    def test_create_stripe_customer_for_user(self, db: Session, user: User):
        assert not user.stripe_customer_id
        create_stripe_customer_for_user(db, user)
        assert user.stripe_customer_id.startswith("cus_")
        with pytest.raises(Exception):
            create_stripe_customer_for_user(db, user)

    def test_get_stripe_subscriptions_for_user(self, user: User):
        assert len(get_stripe_subscriptions_for_user(user)) == 0

    def test_get_user_from_customer_id(self, db: Session, user: User):
        assert get_user_from_stripe_customer_id(db, user.stripe_customer_id) == user

    def test_get_stripe_prices(self):
        prices = get_stripe_prices()
        assert len(list(prices.keys())) == 3

    def test_create_checkout_session(self, user: User):
        session = create_checkout_session("http://localhost", Plan.LITE, user)
        assert session.url

    def test_create_portal(self, user: User):
        portal = get_portal_session("http://localhost", user)
        assert portal.url
