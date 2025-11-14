from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

from . import db, stripe_routes, auth_routes
from . import rag, workflows
from .assistants import (
    leadforge,
    invoicevision,
    regwatch,
    taskflow,
    knowbase,
    qcrisk,
    clientpulse,
    salesgen,
    finres,
    docguard,
    hrbuddy,
    projman,
    datascout,
    marketlens,
    supportdesk,
    diarybuddy,
    focusinbox,
    meetscribe,
    docdraft,
    uxcopy,
    csplaybook,
    seoarchitect,
    supplychainpro,
    rendercraft,
    flowdesigner,
    onboardingcoach,
    riskscenario,
    cohortanalyst,
    excelwizard,
    pricelens,
    forecastlab,
    opsdoctrine,
    processflow,
    finstatanalyst,
    fcaregwatch,
    policydraftfca,
    pensionscenario,
    portfoliostress,
    globalrisk,
)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(title="Servination AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.init()


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/pricing", include_in_schema=False)
def pricing_page():
    pricing_path = os.path.join(FRONTEND_DIR, "pricing.html")
    return FileResponse(pricing_path)


@app.get("/terms", include_in_schema=False)
def terms_page():
    terms_path = os.path.join(FRONTEND_DIR, "terms.html")
    return FileResponse(terms_path)


@app.get("/assistants", include_in_schema=False)
def assistants_page():
    assistants_path = os.path.join(FRONTEND_DIR, "assistants.html")
    return FileResponse(assistants_path)


@app.get("/signup", include_in_schema=False)
async def signup_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "signup.html"))


@app.get("/plans/bronze", include_in_schema=False)
async def plan_bronze_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "plan_bronze.html"))


@app.get("/plans/standard", include_in_schema=False)
async def plan_standard_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "plan_standard.html"))


@app.get("/plans/gold", include_in_schema=False)
async def plan_gold_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "plan_gold.html"))


@app.get("/plans/platinum", include_in_schema=False)
async def plan_platinum_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "plan_platinum.html"))


@app.get("/plans/diamond", include_in_schema=False)
async def plan_diamond_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "plan_diamond.html"))



@app.get("/case-studies", include_in_schema=False)

@app.get("/rag", include_in_schema=False)
async def rag_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "rag.html"))


@app.get("/workflows", include_in_schema=False)
async def workflows_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "workflows.html"))


@app.get("/reports", include_in_schema=False)
async def reports_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "reports.html"))

async def case_studies_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "case_studies.html"))


@app.get("/client", include_in_schema=False)
async def client_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "client.html"))


# Assistant routers
app.include_router(leadforge.router)
app.include_router(invoicevision.router)
app.include_router(regwatch.router)
app.include_router(taskflow.router)
app.include_router(knowbase.router)
app.include_router(qcrisk.router)
app.include_router(clientpulse.router)
app.include_router(salesgen.router)
app.include_router(finres.router)
app.include_router(docguard.router)
app.include_router(hrbuddy.router)
app.include_router(projman.router)
app.include_router(datascout.router)
app.include_router(marketlens.router)
app.include_router(supportdesk.router)
app.include_router(diarybuddy.router)
app.include_router(focusinbox.router)
app.include_router(meetscribe.router)
app.include_router(docdraft.router)
app.include_router(uxcopy.router)
app.include_router(csplaybook.router)
app.include_router(seoarchitect.router)
app.include_router(supplychainpro.router)
app.include_router(rendercraft.router)
app.include_router(flowdesigner.router)
app.include_router(onboardingcoach.router)
app.include_router(riskscenario.router)
app.include_router(cohortanalyst.router)
app.include_router(excelwizard.router)
app.include_router(pricelens.router)
app.include_router(forecastlab.router)
app.include_router(opsdoctrine.router)
app.include_router(processflow.router)
app.include_router(finstatanalyst.router)
app.include_router(fcaregwatch.router)
app.include_router(policydraftfca.router)
app.include_router(pensionscenario.router)
app.include_router(portfoliostress.router)
app.include_router(globalrisk.router)

app.include_router(rag.router)
app.include_router(workflows.router)

app.include_router(stripe_routes.router)
app.include_router(auth_routes.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
