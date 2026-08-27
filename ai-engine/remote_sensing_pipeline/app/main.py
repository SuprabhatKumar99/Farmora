from fastapi import FastAPI

from app.remote_sensing.api.routes import configure_service, router
from app.remote_sensing.services.service import RemoteSensingService
from app.remote_sensing.storage.local import LocalRemoteSensingStorage


storage = LocalRemoteSensingStorage("data/media/remote_sensing")
service = RemoteSensingService(storage=storage)

configure_service(service)

app = FastAPI(
    title="Agricultural AI Engine — Remote Sensing Pipeline",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "remote-sensing-pipeline",
    }


@app.get("/ready")
def ready():
    return {"status": "READY"}
