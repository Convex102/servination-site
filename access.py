from fastapi import HTTPException

# Simple rank system so higher tiers automatically include lower tiers.
PLAN_RANK = {
    "standard": 1,
    "bronze": 2,
    "silver": 3,   # kept for compatibility if older rows exist
    "gold": 4,
    "platinum": 5,
    "diamond": 6,
    "enterprise": 7,
}

# Minimum required plan for each assistant.
ASSISTANT_MIN_PLAN = {
    # Standard – core personal productivity
    "diarybuddy": "standard",
    "focusinbox": "standard",
    "meetscribe": "standard",
    "docdraft": "standard",
    "uxcopy": "standard",
    "excelwizard": "standard",

    # Bronze – small teams across support and knowledge
    "csplaybook": "bronze",
    "knowbase": "bronze",
    "supportdesk": "bronze",
    "hrbuddy": "bronze",

    # Gold – broader business operations, risk, finance, sales, processes
    "leadforge": "gold",
    "invoicevision": "gold",
    "regwatch": "gold",
    "taskflow": "gold",
    "qcrisk": "gold",
    "clientpulse": "gold",
    "salesgen": "gold",
    "finres": "gold",
    "docguard": "gold",
    "projman": "gold",
    "datascout": "gold",
    "marketlens": "gold",
    "seoarchitect": "gold",
    "supplychainpro": "gold",
    "rendercraft": "gold",
    "flowdesigner": "gold",
    "onboardingcoach": "gold",
    "pricelens": "gold",
    "opsdoctrine": "gold",
    "processflow": "gold",
    "finstatanalyst": "gold",
    "fcaregwatch": "gold",
    "policydraftfca": "gold",

    # Platinum – advanced scenario, pensions & retention analytics
    "riskscenario": "platinum",
    "cohortanalyst": "platinum",
    "pensionscenario": "platinum",
    "portfoliostress": "platinum",

    # Diamond – state-of-the-art HMM–CNN–BiLSTM-style forecasting
    "forecastlab": "diamond",
    "globalrisk": "diamond",
}


def ensure_allowed(plan: str | None, assistant_key: str):
    """Raise if the user's plan does not allow access to the assistant.

    Enterprise is treated as highest tier and can access everything.
    Unknown plans fall back to 'standard'.
    """
    if not assistant_key:
        return

    required = ASSISTANT_MIN_PLAN.get(assistant_key)
    if not required:
        # If an assistant isn't explicitly mapped, treat it as standard.
        required = "standard"

    if not plan:
        plan = "standard"

    # Normalise & handle enterprise
    plan = plan.lower().strip()
    if plan == "enterprise":
        return

    user_rank = PLAN_RANK.get(plan, 1)
    required_rank = PLAN_RANK.get(required, 1)

    if user_rank < required_rank:
        raise HTTPException(
            status_code=403,
            detail=f"Your plan '{plan}' does not include access to the '{assistant_key}' assistant. "
                   f"Minimum required plan is '{required}'. Please upgrade to use this capability.",
        )
