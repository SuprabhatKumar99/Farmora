from fastapi import FastAPI

from app.decision_outputs.api.routes import router

app = FastAPI(
    title="Agricultural AI Engine — Step 17 Decision Outputs"
)
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "component": "DECISION_RISK_RECOMMENDATION_OUTPUTS",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
