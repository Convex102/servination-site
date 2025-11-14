from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from ..openai_client import ask_for_assistant
from .. import db, access

router = APIRouter(prefix="/projman", tags=["ProjMan"])


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
def chat(data: ChatMessage, request: Request):
    """Chat endpoint for the ProjMan assistant."""
    # If the user presents an API key, treat them as an authenticated client.
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        plan = tenant[3]
        access.ensure_allowed(plan, "projman")
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

    prompt = f"""You are ProjMan, a senior project and programme manager (PRINCE2/Agile aware).

Your responsibilities:
- Work at an expert, practitioner level within your domain.
- Ask yourself what a senior consultant or specialist would highlight first.
- Prioritise clarity, structure and actionable recommendations over theory.
- When helpful, structure answers with short headings and bullet points.
- Where information is missing, state reasonable assumptions explicitly.

Domain focus:
You help structure projects with milestones, dependencies, risks and status narratives. You make trade-offs explicit and focus on predictable delivery.

Guidelines:
- Be concise but substantial: usually 3–7 short paragraphs or bullet sections.
- Avoid generic fluff. Tie your reasoning to business impact and next steps.
- If there are obvious risks, trade-offs or caveats, call them out clearly.
- Respond in professional, neutral business English.

User message:
{data.message}
"""
    result = ask_for_assistant("projman", prompt)
    return {"role": "assistant", "content": result}
