from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from ..openai_client import ask_for_assistant
from .. import db, access
from ..rag_utils import embed_text

router = APIRouter(prefix="/knowbase", tags=["KnowBase"])


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
def chat(data: ChatMessage, request: Request):
    """Chat endpoint for the KnowBase assistant with vector RAG + lightweight memory."""
    # If the user presents an API key, treat them as an authenticated client.
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    tenant_id = None
    ip = None

    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        plan = tenant[3]
        access.ensure_allowed(plan, "knowbase")
        tenant_id = tenant[0]
    else:
        # Anonymous 'sample' usage is limited to 2 calls per IP address.
        ip = request.client.host or "unknown"
        uses = db.increment_ip_usage(ip)
        if uses > 2:
            raise HTTPException(
                status_code=402,
                detail=(
                    "Free sample limit reached for this device. "
                    "Please start a Servination trial to continue using the assistants."
                ),
            )

    # Load recent conversational memory
    history_entries = db.get_recent_memory(tenant_id, ip, "knowbase", limit=6)
    history_blocks = []
    for role, content in history_entries:
        prefix = "User" if role == "user" else "Assistant"
        history_blocks.append(f"{prefix}: {content}")
    history_text = "\n".join(history_blocks)

    # Simple RAG: search tenant-specific knowledge docs before answering
    context_text = ""
    try:
        query_embedding = embed_text(data.message)
        if query_embedding:
            docs = db.query_knowledge_docs(
                tenant_id=tenant_id,
                assistant="knowbase",
                query_embedding=query_embedding,
                top_k=5,
            )
            if docs:
                context_chunks = []
                for d in docs:
                    title = d.get("title") or ""
                    text = d.get("text") or ""
                    context_chunks.append(f"[{title}]\n{text}")
                context_text = "\n\n".join(context_chunks)
    except Exception:
        # Fail open – if RAG fails we still answer based on prompt alone.
        context_text = ""

    prompt = f"""You are KnowBase, an internal knowledge management and policy-explainer assistant.

Your responsibilities:
- Work at an expert, practitioner level within your domain.
- Ask yourself what a senior consultant or specialist would highlight first.
- Prioritise clarity, structure and actionable recommendations over theory.
- When helpful, structure answers with short headings and bullet points.
- Where information is missing, state reasonable assumptions explicitly.

Domain focus:
You answer questions about internal policies, procedures and documentation. When helpful, you suggest how a real organisation could structure or clarify its policies.

Guidelines:
- Be concise but substantial: usually 3–7 short paragraphs or bullet sections.
- Avoid generic fluff. Tie your reasoning to business impact and next steps.
- If there are obvious risks, trade-offs or caveats, call them out clearly.
- Respond in professional, neutral business English.

Conversation so far (may be empty):
{history_text}

Knowledge documents (may be empty):
{context_text}

User message:
{data.message}
"""
    result = ask_for_assistant("knowbase", prompt)

    # Persist memory for future turns
    db.add_memory(tenant_id, ip, "knowbase", "user", data.message)
    db.add_memory(tenant_id, ip, "knowbase", "assistant", result)

    return {"role": "assistant", "content": result}
