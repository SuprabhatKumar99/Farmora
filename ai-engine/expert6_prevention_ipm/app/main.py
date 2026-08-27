from fastapi import FastAPI

from app.experts.expert6_prevention_ipm.api.routes import router

app = FastAPI(title="Agricultural AI Engine — Expert 6")
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "expert": "EXPERT_6_PREVENTION_IPM",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
