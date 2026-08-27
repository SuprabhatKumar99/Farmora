from pathlib import Path

from fastapi import FastAPI

from app.observation.api.routes import configure_service, router
from app.observation.media.validator import MediaValidator
from app.observation.services.service import ObservationService
from app.observation.storage.local import LocalMediaStorage


STORAGE_DIR = Path("data/media")

storage = LocalMediaStorage(STORAGE_DIR)
validator = MediaValidator()
service = ObservationService(storage, validator)

configure_service(service)

app = FastAPI(
    title="Agricultural AI Engine — Observation Pipeline",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "observation-pipeline",
    }


@app.get("/ready")
def ready():
    return {
        "status": "READY",
    }
