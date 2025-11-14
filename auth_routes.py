import os
import secrets

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from . import db, pricing

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupRequest(BaseModel):
    name: str
    email: str
    plan: str  # bronze | standard | gold | platinum | diamond | enterprise
    session_id: str  # Stripe Checkout session id from the successful subscription checkout


class SignupResponse(BaseModel):
    api_key: str
    plan: str


class LoginRequest(BaseModel):
    email: str
    api_key: str


class LoginResponse(BaseModel):
    name: str
    email: str
    plan: str


@router.post("/signup", response_model=SignupResponse)
def signup(payload: SignupRequest):
    """Create a tenant + API key after a successful Stripe checkout session.

    This endpoint now enforces that a valid Stripe Checkout session has completed
    before an API key can be generated, so you cannot bypass billing to obtain access.
    """
    plan_key = payload.plan.lower().strip()
    if plan_key not in pricing.PLANS:
        raise HTTPException(status_code=400, detail="Unknown plan selected.")

    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Stripe is not configured on the server. Please set STRIPE_SECRET_KEY.",
        )

    if not payload.session_id:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe checkout session_id. Complete checkout before creating an API key.",
        )

    # Validate the Stripe Checkout session
    try:
        session = stripe.checkout.Session.retrieve(payload.session_id)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Stripe session. Please restart checkout. ({exc})",
        ) from exc

    if session.mode != "subscription":
        raise HTTPException(
            status_code=400,
            detail="Stripe session is not a subscription checkout.",
        )

    # For a successful subscription with trial, status should be 'complete'
    if getattr(session, "status", None) != "complete":
        raise HTTPException(
            status_code=400,
            detail="Stripe checkout has not completed yet. Please finish the payment step first.",
        )

    # In a more advanced setup you would also confirm that the subscribed price
    # matches the selected plan. For this demo we rely on the client correctly
    # pairing plans to Stripe price ids.

    api_key = secrets.token_hex(16)
    plan_cfg = pricing.PLANS[plan_key]
    credits = plan_cfg.get("included_tokens") or 0

    db.create_tenant(payload.name, payload.email, plan_key, api_key, credits)
    return SignupResponse(api_key=api_key, plan=plan_key)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """Simple API key + email based login to the client workspace."""
    row = db.verify_key(payload.api_key.strip())
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    _id, name, email, plan, key, _credits = row
    if email.lower().strip() != payload.email.lower().strip():
        raise HTTPException(status_code=403, detail="Email does not match this API key.")

    return LoginResponse(name=name, email=email, plan=plan)
