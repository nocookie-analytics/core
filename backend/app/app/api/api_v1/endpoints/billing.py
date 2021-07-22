from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.datastructures import URLPath
from starlette.requests import Request
from starlette.responses import Response

from app import models, schemas
from app.api import deps
from app.core.config import settings
from app.core.products import Plan
import stripe

router = APIRouter()


@router.get("/subscribe", response_model=schemas.SignupLink)
def subscribe(
    *,
    db: Session = Depends(deps.get_db),
    plan_name: Plan,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Subscribe to a plan
    """
    cancel_url = URLPath("/main/billing/cancelled").make_absolute_url(request.base_url)
    success_url = URLPath("/main/billing/success").make_absolute_url(request.base_url)
    price_list = stripe.Price.list(lookup_keys=[e.value for e in Plan])
    price_map = {
        Plan(price_object.lookup_key): price_object
        for price_object in price_list["data"]
    }

    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[
            {
                "price": price_map[plan_name].id,
                "quantity": 1,
            }
        ],
        subscription_data={"trial_period_days": 14},
        client_reference_id=current_user.id,
        customer_email=current_user.email,
    )
    return {"url": session.url}


@router.post("/webhook")
async def webhook_received(request: Request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    body = await request.body()
    request_data = await request.json()

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                payload=body, sig_header=signature, secret=webhook_secret
            )
            data = event["data"]
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]

    if event_type == "checkout.session.completed":
        # Payment is successful and the subscription is created.
        # You should provision the subscription and save the customer ID to your database.
        print(data)
    elif event_type == "invoice.paid":
        # Continue to provision the subscription as payments continue to be made.
        # Store the status in your database and check when a user accesses your service.
        # This approach helps you avoid hitting rate limits.
        print(data)
    elif event_type == "invoice.payment_failed":
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        print(data)
    else:
        print("Unhandled event type {}".format(event_type))

    return Response({"status": "success"})
