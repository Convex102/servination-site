"""Pricing configuration for Servination plans.

This module does not perform billing, but centralises the conceptual
rules so they can be enforced consistently by background jobs or Stripe
webhooks in a real deployment.
"""

EXCESS_MARKUP = 1.02  # 2% above underlying model cost price

PLANS = {
    "standard": {
        "name": "Standard",
        "price_gbp": 39.99,
        "max_assistants": 3,
        "included_tokens": 150_000,
    },
    "bronze": {
        "name": "Bronze",
        "price_gbp": 99.99,
        "max_assistants": 8,
        "included_tokens": 500_000,
    },
    "gold": {
        "name": "Gold",
        "price_gbp": 250.00,
        "max_assistants": 20,
        "included_tokens": 2_000_000,
    },
    "platinum": {
        "name": "Platinum",
        "price_gbp": 499.00,
        "max_assistants": 30,
        "included_tokens": 4_000_000,
    },
    "diamond": {
        "name": "Diamond",
        "price_gbp": 750.00,
        "max_assistants": 30,
        "included_tokens": 8_000_000,
    },
    "enterprise": {
        "name": "Enterprise",
        "price_gbp": None,
        "max_assistants": None,  # Custom
        "included_tokens": None,  # Custom
    },
}
