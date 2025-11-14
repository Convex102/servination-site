from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict

from . import db
from .openai_client import ask_for_assistant

router = APIRouter(prefix="/workflows", tags=["Workflows"])


class WorkflowStep(BaseModel):
    assistant: str
    input: str
    key: Optional[str] = None  # optional key name to store this step's output


class WorkflowRequest(BaseModel):
    steps: List[WorkflowStep]


@router.post("/run")
def run_workflow(payload: WorkflowRequest, request: Request):
    """Execute a simple multi-step workflow across multiple assistants.

    Each step is run sequentially. The output of all previous steps is made available
    as context to the next step. This provides a lightweight workflow automation layer
    over the Servination assistants.
    """
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")

    context_log: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []

    for idx, step in enumerate(payload.steps):
        # Build a context string from prior steps
        context_lines = []
        for prev in context_log:
            ctx_key = prev.get("key") or f"step_{prev['index']}"
            ctx_short = prev.get("output", "")[:800]
            context_lines.append(f"{ctx_key}: {ctx_short}")
        context_text = "\n".join(context_lines)

        prompt = (
            f"You are the '{step.assistant}' assistant inside the Servination multi-agent platform.\n"
            f"Previous workflow context (may be empty):\n{context_text}\n\n"
            f"Current step ({idx + 1}) input:\n{step.input}\n\n"
            "Use the previous context where helpful, but focus on producing the best possible output for this step."
        )

        output = ask_for_assistant(step.assistant, prompt)
        step_key = step.key or f"step_{idx + 1}"

        context_log.append(
            {
                "index": idx + 1,
                "assistant": step.assistant,
                "key": step_key,
                "output": output,
            }
        )
        results.append(
            {
                "index": idx + 1,
                "assistant": step.assistant,
                "key": step_key,
                "output": output,
            }
        )

    return {"steps": results}
