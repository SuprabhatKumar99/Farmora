from fastapi import FastAPI

from app.experts.expert7_treatment_management.api.routes import router

app = FastAPI(title="Agricultural AI Engine — Expert 7")
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "expert": "EXPERT_7_TREATMENT_MANAGEMENT",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
