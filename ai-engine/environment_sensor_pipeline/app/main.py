from fastapi import FastAPI

from app.environment.api.routes import configure_service, router
from app.environment.services.service import EnvironmentSensorService
from app.environment.storage.in_memory import InMemorySensorStore


store = InMemorySensorStore()
service = EnvironmentSensorService(store)
configure_service(service)

app = FastAPI(
    title="Agricultural AI Engine — Environment & Sensor Pipeline",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "environment-sensor-pipeline",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
