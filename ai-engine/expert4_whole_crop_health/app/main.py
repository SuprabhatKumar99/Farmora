from fastapi import FastAPI

from app.experts.expert4_whole_crop_health.api.routes import router

app = FastAPI(title="Agricultural AI Engine — Expert 4")
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "expert": "EXPERT_4_WHOLE_CROP_HEALTH",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
