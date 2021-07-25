from typing import Any, Dict, List, Tuple, Union
from sqlalchemy.orm.session import Session
from starlette.datastructures import URL, URLPath
from starlette.requests import Request
from app.core.config import settings

from app import crud
from app.core.products import Plan
from app.models.user import User
from app.schemas.user import UserStripeInfoUpdate
import stripe


def create_stripe_customer_for_user(db: Session, user_obj: User) -> None:
    if user_obj.stripe_customer_id:
        raise Exception("This user already has a customer id")
    customer = stripe.Customer.create(
        email=user_obj.email,
        metadata={"user_id": user_obj.id},
        name=user_obj.full_name,
    )
    stripe_info_update = UserStripeInfoUpdate(stripe_customer_id=customer.id)
    crud.user.update_stripe_info(db, user_obj=user_obj, obj_in=stripe_info_update)


def get_stripe_subscriptions_for_user(user_obj: User) -> List:
    subscriptions = stripe.Subscription.list(customer=user_obj.stripe_customer_id)
    return subscriptions.data


def cancel_stripe_subscription(db: Session, user_obj: User) -> None:
    subscription = stripe.Subscription.list(customer=user_obj.stripe_customer_id)
    stripe.Subscription.delete(subscription.data[0].id)
    stripe_info_update = UserStripeInfoUpdate(
        active_plan=Plan.CANCELLED, stripe_subscription_ref=None
    )
    crud.user.update_stripe_info(db, user_obj=user_obj, obj_in=stripe_info_update)


def get_user_from_stripe_customer_id(db: Session, customer_id: str) -> User:
    return db.query(User).filter(User.stripe_customer_id == customer_id).scalar()


def get_stripe_prices() -> Dict[Plan, str]:
    price_list = stripe.Price.list(lookup_keys=[e.value for e in Plan])
    price_map = {
        Plan(price_object.lookup_key): price_object.id
        for price_object in price_list["data"]
    }
    return price_map


def create_checkout_session(base_url: Union[str, URL], plan: Plan, user: User) -> str:
    """Get a URL for a checkout session"""
    cancel_url = URLPath("/main/transaction/cancelled").make_absolute_url(base_url)
    success_url = URLPath("/main/transaction/success").make_absolute_url(base_url)
    prices = get_stripe_prices()

    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        customer=user.stripe_customer_id,
        payment_method_types=["card"],
        mode="subscription",
        metadata={"plan": plan.value},
        line_items=[
            {
                "price": prices[plan],
                "quantity": 1,
            }
        ],
        subscription_data={"trial_period_days": 14},
    )
    return session.url


def get_portal_session_url(base_url: Union[str, URL], user: User) -> str:
    return_url = URLPath("/main/").make_absolute_url(base_url)
    session = stripe.billing_portal.Session.create(
        customer=user.stripe_customer_id,
        return_url=return_url,
    )
    return session.url


def verify_webhook(body, signature) -> Tuple[str, Any]:
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload=body, sig_header=signature, secret=webhook_secret
        )
        event_type, data = event["data"]
    except Exception as e:
        raise e
    return event_type, data
