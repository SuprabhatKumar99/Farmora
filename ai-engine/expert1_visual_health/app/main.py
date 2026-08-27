from fastapi import FastAPI
from app.experts.expert1_visual_health.api.routes import router

app = FastAPI(
    title="Agricultural AI Engine — Expert 1 Visual Health",
    version="0.1.0"
)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "UP", "expert": "EXPERT_1_VISUAL_HEALTH"}

@app.get("/ready")
def ready():
    return {"status": "READY"}
