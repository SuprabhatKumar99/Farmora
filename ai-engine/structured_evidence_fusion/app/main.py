from fastapi import FastAPI
from app.evidence_fusion.api.routes import router

app=FastAPI(title="Agricultural AI Engine — Structured Evidence Fusion")
app.include_router(router)

@app.get("/health")
def health():
    return {"status":"UP","component":"STRUCTURED_EVIDENCE_FUSION"}

@app.get("/ready")
def ready():
    return {"status":"READY"}
