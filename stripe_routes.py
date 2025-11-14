import os

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/billing", tags=["Billing"])


class CheckoutRequest(BaseModel):
    plan: str  # "standard" | "bronze" | "silver" | "gold" | "platinum" | "diamond"


_PLAN_ENV = {
    "standard": "STRIPE_PRICE_STANDARD",
    "bronze": "STRIPE_PRICE_BRONZE",
    "silver": "STRIPE_PRICE_SILVER",
    "gold": "STRIPE_PRICE_GOLD",
    "platinum": "STRIPE_PRICE_PLATINUM",
    "diamond": "STRIPE_PRICE_DIAMOND",
}


@router.post("/checkout")
def create_checkout_session(payload: CheckoutRequest):
    """Create a Stripe Checkout session for a subscription with a 30-day trial.

    This expects the following environment variables to be set:

    - STRIPE_SECRET_KEY
    - STRIPE_PRICE_STANDARD
    - STRIPE_PRICE_BRONZE
    - STRIPE_PRICE_SILVER
    - STRIPE_PRICE_GOLD
    - STRIPE_PRICE_PLATINUM
    - STRIPE_PRICE_DIAMOND
    - STRIPE_SUCCESS_URL (optional, defaults to http://localhost:8000/)
    - STRIPE_CANCEL_URL (optional, defaults to http://localhost:8000/pricing)
    """
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe is not configured on the server.")

    plan_key = payload.plan.lower().strip()
    env_var = _PLAN_ENV.get(plan_key)
    if not env_var:
        raise HTTPException(status_code=400, detail="Unknown plan requested.")

    price_id = os.getenv(env_var)
    if not price_id:
        raise HTTPException(
            status_code=500,
            detail=f"Stripe price for plan '{plan_key}' is not configured. Set {env_var}.",
        )

    success_url = os.getenv("STRIPE_SUCCESS_URL", "http://localhost:8000/signup")
    cancel_url = os.getenv("STRIPE_CANCEL_URL", "http://localhost:8000/pricing")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            subscription_data={
                "trial_period_days": 30,
            },
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Unable to create Stripe session: {exc}") from exc

    return {"id": session.id, "url": session.url}
