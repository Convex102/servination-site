from typing import List
from . import openai_client as oc

# Simple embedding helper using OpenAI's text-embedding-3-small model.
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str) -> List[float]:
    """Return an embedding vector for the given text using OpenAI embeddings.

    If OpenAI is not configured, returns an empty list so callers can handle gracefully.
    """
    if getattr(oc, "_openai_client", None) is None:
        return []
    try:
        res = oc._openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[text],
        )
        return res.data[0].embedding  # type: ignore[attr-defined]
    except Exception:
        return []


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Batch embed multiple texts."""
    return [embed_text(t) for t in texts]
