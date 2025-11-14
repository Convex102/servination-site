import os
from typing import Dict
from dotenv import load_dotenv

# Optional providers
try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI = None

try:
    import anthropic as _anthropic
except ImportError:
    _anthropic = None

try:
    import google.generativeai as _genai
except ImportError:
    _genai = None

try:
    import cohere as _cohere
except ImportError:
    _cohere = None

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

_openai_client = _OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and _OpenAI else None
_anthropic_client = _anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY and _anthropic else None
if _genai and GEMINI_API_KEY:
    _genai.configure(api_key=GEMINI_API_KEY)
_cohere_client = _cohere.Client(api_key=COHERE_API_KEY) if COHERE_API_KEY and _cohere else None

# Assistant -> model routing
# Model keys are of the form "<provider>:<model_name>"
# Providers: openai, anthropic, gemini, cohere
ASSISTANT_MODEL_MAP: Dict[str, str] = {
    # Sales / marketing / outreach
    "leadforge": "openai:gpt-4.1-mini",
    "salesgen": "openai:gpt-4.1-mini",
    "clientpulse": "openai:gpt-4.1-mini",
    "marketlens": "openai:gpt-4.1-mini",
    "datascout": "openai:gpt-4.1-mini",
    "supportdesk": "openai:gpt-4.1-mini",
    "docdraft": "openai:gpt-4.1-mini",
    "uxcopy": "openai:gpt-4.1-mini",
    "csplaybook": "openai:gpt-4.1-mini",
    "seoarchitect": "openai:gpt-4.1-mini",

    # Ops / HR / project / process assistants
    "taskflow": "openai:gpt-4.1-mini",
    "hrbuddy": "openai:gpt-4.1-mini",
    "projman": "openai:gpt-4.1-mini",
    "diarybuddy": "openai:gpt-4.1-mini",
    "focusinbox": "openai:gpt-4.1-mini",
    "meetscribe": "openai:gpt-4.1-mini",
    "supplychainpro": "openai:gpt-4.1-mini",
    "rendercraft": "openai:gpt-4.1-mini",
    "flowdesigner": "openai:gpt-4.1-mini",
    "onboardingcoach": "openai:gpt-4.1-mini",
    "opsdoctrine": "openai:gpt-4.1-mini",
    "processflow": "openai:gpt-4.1-mini",

    # Knowledge / document safety
    "knowbase": "cohere:command-r-plus",
    "docguard": "cohere:command-r-plus",

    # Finance / analytics / forecasting
    "invoicevision": "gemini:gemini-1.5-pro",
    "finres": "gemini:gemini-1.5-pro",
    "finstatanalyst": "gemini:gemini-1.5-pro",
    "excelwizard": "openai:gpt-4.1-mini",
    "cohortanalyst": "gemini:gemini-1.5-pro",
    "pricelens": "gemini:gemini-1.5-pro",
    "forecastlab": "gemini:gemini-1.5-pro",

    # Risk, FCA, pensions & global risk
    "regwatch": "anthropic:claude-3.5-sonnet",
    "qcrisk": "anthropic:claude-3.5-sonnet",
    "riskscenario": "anthropic:claude-3.5-sonnet",
    "globalrisk": "anthropic:claude-3.5-sonnet",
    "portfoliostress": "anthropic:claude-3.5-sonnet",
    "fcaregwatch": "anthropic:claude-3.5-sonnet",
    "policydraftfca": "anthropic:claude-3.5-sonnet",
    "pensionscenario": "anthropic:claude-3.5-sonnet",
}

DEFAULT_MODEL_KEY = "openai:gpt-4.1-mini"


def _ask_openai(model_name: str, prompt: str) -> str:
    if _openai_client is None:
        return "(OpenAI not configured - set OPENAI_API_KEY in .env)\nPrompt preview: " + prompt[:200]
    try:
        res = _openai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return (res.choices[0].message.content or "").strip()
    except Exception as e:
        return f"(OpenAI error: {e})"


def _ask_anthropic(model_name: str, prompt: str) -> str:
    if _anthropic_client is None:
        # Fallback to OpenAI if Anthropic not available
        return _ask_openai("gpt-4.1-mini", prompt)
    try:
        res = _anthropic_client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        # Anthropic returns content as a list of blocks
        parts = []
        for block in getattr(res, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
        return "\n".join(parts).strip() if parts else str(res)
    except Exception as e:
        return f"(Anthropic error, falling back to OpenAI) {e}\n" + _ask_openai("gpt-4.1-mini", prompt)


def _ask_gemini(model_name: str, prompt: str) -> str:
    if _genai is None or not GEMINI_API_KEY:
        return _ask_openai("gpt-4.1-mini", prompt)
    try:
        model = _genai.GenerativeModel(model_name)
        res = model.generate_content(prompt)
        return (getattr(res, "text", None) or "").strip()
    except Exception as e:
        return f"(Gemini error, falling back to OpenAI) {e}\n" + _ask_openai("gpt-4.1-mini", prompt)


def _ask_cohere(model_name: str, prompt: str) -> str:
    if _cohere_client is None:
        return _ask_openai("gpt-4.1-mini", prompt)
    try:
        res = _cohere_client.chat(model=model_name, message=prompt)
        return (getattr(res, "text", None) or "").strip()
    except Exception as e:
        return f"(Cohere error, falling back to OpenAI) {e}\n" + _ask_openai("gpt-4.1-mini", prompt)


def ask_with_model(model_key: str, prompt: str) -> str:
    """Low-level entrypoint: call a specific model key like 'openai:gpt-4.1-mini'."""
    provider, model_name = (model_key or DEFAULT_MODEL_KEY).split(":", 1)
    provider = provider.lower().strip()

    if provider == "openai":
        return _ask_openai(model_name, prompt)
    if provider == "anthropic":
        return _ask_anthropic(model_name, prompt)
    if provider == "gemini":
        return _ask_gemini(model_name, prompt)
    if provider == "cohere":
        return _ask_cohere(model_name, prompt)

    # Unknown provider: default to OpenAI
    return _ask_openai("gpt-4.1-mini", prompt)


def ask_for_assistant(assistant_slug: str, prompt: str) -> str:
    """Route a prompt based on the assistant slug (e.g. 'leadforge', 'regwatch')."""
    key = ASSISTANT_MODEL_MAP.get(assistant_slug, DEFAULT_MODEL_KEY)
    return ask_with_model(key, prompt)


# Backwards-compatible helper: default to the platform default model
def ask(prompt: str) -> str:
    """Legacy entrypoint used by older assistants; uses the default model."""
    return ask_with_model(DEFAULT_MODEL_KEY, prompt)
