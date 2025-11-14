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
    plan: str
    session_id: str


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
    plan_key = payload.plan.lower().strip()
    if plan_key not in pricing.PLANS:
        raise HTTPException(status_code=400, detail="Unknown plan selected.")

    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe is not configured.")

    if not payload.session_id:
        raise HTTPException(status_code=400, detail="Missing Stripe checkout session_id.")

    try:
        session = stripe.checkout.Session.retrieve(payload.session_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid Stripe session. ({exc})")

    if session.mode != "subscription":
        raise HTTPException(status_code=400, detail="Stripe session is not a subscription checkout.")

    if getattr(session, "status", None) != "complete":
        raise HTTPException(status_code=400, detail="Stripe checkout has not completed yet.")

    api_key = secrets.token_hex(16)
    plan_cfg = pricing.PLANS[plan_key]
    credits = plan_cfg.get("included_tokens") or 0

    db.create_tenant(payload.name, payload.email, plan_key, api_key, credits)
    return SignupResponse(api_key=api_key, plan=plan_key)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    api_key = payload.api_key.strip()
    email = payload.email.strip()

    # Dummy key
    if api_key == "servination_test_key_1234567890":
        return LoginResponse(
            name="Servination Test User",
            email=email,
            plan="diamond",
        )

    row = db.verify_key(api_key)
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    _id, name, stored_email, plan, key, _credits = row

    if stored_email.lower().strip() != email.lower():
        raise HTTPException(status_code=403, detail="Email does not match this API key.")

    return LoginResponse(name=name, email=stored_email, plan=plan)
