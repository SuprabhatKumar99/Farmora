from fastapi import FastAPI

from app.disease_events.api.routes import configure_service, router
from app.disease_events.services.service import DiseaseEventService
from app.disease_events.storage.in_memory import InMemoryDiseaseEventStore


store = InMemoryDiseaseEventStore()
service = DiseaseEventService(store)

configure_service(service)

app = FastAPI(
    title="Agricultural AI Engine — Disease Event & Progression Engine",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "disease-event-progression-engine",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
