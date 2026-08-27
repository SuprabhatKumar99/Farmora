from fastapi import FastAPI

from app.followup_feedback.api.routes import router

app = FastAPI(
    title="Agricultural AI Engine — Step 19 Follow-up & Feedback Loop"
)
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "component": "FOLLOWUP_FEEDBACK_LOOP",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
