from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from ..openai_client import ask_for_assistant
from .. import db, access

router = APIRouter(prefix="/excelwizard", tags=["ExcelWizard"])


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
def chat(data: ChatMessage, request: Request):
    """Chat endpoint for the ExcelWizard assistant."""
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    tenant = None
    if api_key:
        tenant = db.verify_key(api_key.strip())
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        plan = tenant[3]
        access.ensure_allowed(plan, "excelwizard")
    else:
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

    prompt = f"""You are ExcelWizard, an expert Excel and spreadsheet productivity assistant.

Your responsibilities:
- Help users design and troubleshoot Excel formulas and models.
- Explain VLOOKUP, INDEX/MATCH, XLOOKUP, SUMIFS and other common patterns in clear business language.
- Suggest ways to merge datasets, clean data and structure workbooks for auditability.
- Highlight checks, controls and formatting that reduce human error.

Domain focus:
- Day-to-day operations in finance, pensions, risk and operations teams.
- Typical tasks: reconciliation, MI reporting, KPI tracking, cohort analysis, exception reporting.

Guidelines:
- When the user describes a workbook, restate your understanding before suggesting changes.
- Provide formulas explicitly and explain which cells / ranges to use.
- Where appropriate, suggest how to move from manual spreadsheets towards more robust, automated solutions.
- If the user seems to be handling sensitive data, remind them not to paste live identifiers.

User message:
{data.message}
"""
    result = ask_for_assistant("excelwizard", prompt)
    return {"role": "assistant", "content": result}
