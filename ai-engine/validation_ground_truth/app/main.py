from fastapi import FastAPI

from app.validation_ground_truth.api.routes import router

app = FastAPI(
    title="Agricultural AI Engine — Step 18 Validation & Ground Truth"
)
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "component": "VALIDATION_GROUND_TRUTH",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
