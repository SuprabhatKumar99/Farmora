from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.environment.schemas.models import Sensor, SensorType
from app.environment.services.service import EnvironmentSensorService


router = APIRouter(
    prefix="/api/v1/environment",
    tags=["environment"],
)

_service: EnvironmentSensorService | None = None


class ReadingRequest(BaseModel):
    sensor_id: str
    value: float
    recorded_at: datetime


def configure_service(service):
    global _service
    _service = service


@router.post("/sensors")
def register_sensor(sensor: Sensor):
    if _service is None:
        raise HTTPException(status_code=503, detail="Environment service unavailable")

    return _service.register_sensor(sensor).model_dump(mode="json")


@router.post("/readings")
def ingest_reading(request: ReadingRequest):
    if _service is None:
        raise HTTPException(status_code=503, detail="Environment service unavailable")

    try:
        reading = _service.ingest_reading(
            sensor_id=request.sensor_id,
            value=request.value,
            recorded_at=request.recorded_at,
        )
        return reading.model_dump(mode="json")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/readings")
def list_readings():
    if _service is None:
        raise HTTPException(status_code=503, detail="Environment service unavailable")

    return [
        reading.model_dump(mode="json")
        for reading in _service.list_readings()
    ]
