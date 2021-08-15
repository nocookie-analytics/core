from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.requests import Request
import stripe

from app import crud, models, schemas
from app.api import deps
from app.core.products import Plan
from app.logger import logger
from app.schemas.user import UserStripeInfoUpdate
from app.utils.email import send_trial_ending_email
from app.utils.stripe_helpers import (
    get_portal_session_url,
    get_stripe_prices,
    get_user_from_stripe_customer_id,
    verify_webhook,
)

router = APIRouter()


@router.get("/portal", response_model=schemas.StripeLink)
def portal(
    *,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Get a link to the Stripe portal to manage subscriptions"""
    url = get_portal_session_url(request.base_url, current_user)
    return {"url": url}


@router.post("/webhook", include_in_schema=False)
async def webhook_received(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
):
    body = await request.body()

    # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    signature = request.headers.get("stripe-signature")
    try:
        event_type, data = verify_webhook(body, signature)
    except Exception as e:
        return e

    logger.info("Received webhook %s", event_type)

    if event_type in [
        "checkout.session.completed",
        "customer.subscription.deleted",
        "customer.subscription.updated",
        "invoice.paid",
        "customer.subscription.trial_will_end",
    ]:
        customer = data.object.customer
        subscription = (
            data.object.subscription
            if event_type == "checkout.session.completed"
            else data.object.id
        )
        logger.info("Processing webhook %s %s %s", event_type, customer, subscription)
        user = get_user_from_stripe_customer_id(db, customer)
        update_stripe_info = None
        if (
            event_type == "checkout.session.completed"
            or event_type == "customer.subscription.updated"
        ):
            stripe_subscription = stripe.Subscription.retrieve(subscription)
            stripe_subscription_price_id = stripe_subscription.plan.id
            plan: Optional[Plan] = None
            for plan, price in get_stripe_prices().items():
                if price == stripe_subscription_price_id:
                    break

            if not plan:
                raise Exception("Unknown price used. Failing ungracefully.")

            update_stripe_info = UserStripeInfoUpdate(
                active_plan=plan, stripe_subscription_ref=subscription
            )
        elif event_type == "customer.subscription.deleted":
            update_stripe_info = UserStripeInfoUpdate(
                active_plan=Plan.CANCELLED, stripe_subscription_ref=None
            )
        elif event_type == "invoice.paid":
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            update_stripe_info = UserStripeInfoUpdate(last_paid=datetime.now())
        elif event_type == "customer.subscription.trial_will_end":
            background_tasks.add_task(
                send_trial_ending_email, user.email, user.trial_end_date
            )
        if update_stripe_info:
            crud.user.update_stripe_info(db, user_obj=user, obj_in=update_stripe_info)
    elif event_type == "invoice.payment_failed":
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        logger.warning(data)
    else:
        logger.warning("Unhandled event type {}".format(event_type))

    return {"status": "success"}
