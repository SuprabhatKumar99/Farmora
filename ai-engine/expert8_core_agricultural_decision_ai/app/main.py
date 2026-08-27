from fastapi import FastAPI

from app.expert8_core_ai.api.routes import router

app = FastAPI(title="Agricultural AI Engine — Expert 8")
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "component": "EXPERT_8_CORE_AGRICULTURAL_DECISION_AI",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
