from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from . import db
from .openai_client import ask_for_assistant
from .rag_utils import embed_text

router = APIRouter(prefix="/rag", tags=["RAG"])


class DocumentUpsert(BaseModel):
    assistant: str
    doc_id: str
    title: Optional[str] = ""
    text: str


class RagQuery(BaseModel):
    assistant: str
    query: str
    top_k: int = 5
    return_answer: bool = True


@router.post("/documents")
def upsert_document(payload: DocumentUpsert, request: Request):
    """Store or update a knowledge document for a tenant/assistant.

    This is the write-path for vector RAG. Documents are associated with a tenant (via API key)
    or with an anonymous IP if used without authentication.
    """
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    tenant_id = None
    ip = None

    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        tenant_id = tenant[0]
    else:
        ip = request.client.host or "unknown"

    embedding = embed_text(payload.text)
    db.upsert_knowledge_doc(
        tenant_id=tenant_id,
        assistant=payload.assistant,
        doc_id=payload.doc_id,
        title=payload.title or payload.doc_id,
        text=payload.text,
        embedding=embedding,
    )
    return {"status": "ok"}


@router.post("/query")
def query_rag(payload: RagQuery, request: Request):
    """Query stored documents for a tenant/assistant using semantic search.

    Optionally, the best-matching documents will be passed into the relevant assistant
    model to generate a grounded answer.
    """
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    tenant_id = None
    ip = None

    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        tenant_id = tenant[0]
    else:
        ip = request.client.host or "unknown"

    query_embedding = embed_text(payload.query)
    docs = db.query_knowledge_docs(
        tenant_id=tenant_id,
        assistant=payload.assistant,
        query_embedding=query_embedding,
        top_k=payload.top_k,
    )

    if not payload.return_answer:
        return {"matches": docs}

    # Build a grounded prompt for the chosen assistant
    context_blocks: List[str] = []
    for d in docs:
        title = d.get("title") or ""
        text = d.get("text") or ""
        context_blocks.append(f"[{title}]\n{text}")

    context_text = "\n\n".join(context_blocks)
    prompt = (
        f"You are the '{payload.assistant}' assistant within the Servination platform. "
        f"You answer user questions strictly based on the supplied knowledge documents.\n\n"
        f"Knowledge documents:\n{context_text}\n\n"
        f"User question:\n{payload.query}\n\n"
        "If the answer is not clearly supported by the documents, say so explicitly.\n"
    )

    answer = ask_for_assistant(payload.assistant, prompt)
    return {"answer": answer, "matches": docs}
