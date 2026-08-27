from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.disease_events.schemas.models import EvidenceType
from app.disease_events.services.service import DiseaseEventService


router = APIRouter(
    prefix="/api/v1/disease-events",
    tags=["disease-events"],
)

_service: DiseaseEventService | None = None


class CreateEventRequest(BaseModel):
    farm_id: str
    zone_id: str
    first_observed_at: datetime
    crop_id: str | None = None
    variety_id: str | None = None
    disease_id: str | None = None
    pest_id: str | None = None
    status: str = "OBSERVED"
    severity: float | None = Field(default=None, ge=0.0, le=1.0)


class EvidenceRequest(BaseModel):
    evidence_type: EvidenceType
    reference_id: str
    observed_at: datetime
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    notes: str | None = None


class ProgressionRequest(BaseModel):
    observed_at: datetime
    severity: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)


def configure_service(service):
    global _service
    _service = service


@router.post("")
def create_event(request: CreateEventRequest):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        event = _service.create_event(**request.model_dump())
        return event.model_dump(mode="json")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{event_id}")
def get_event(event_id: str):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        return _service.get_event(event_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Event not found") from exc


@router.post("/{event_id}/evidence")
def add_evidence(event_id: str, request: EvidenceRequest):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        evidence = _service.add_evidence(
            event_id=event_id,
            **request.model_dump(),
        )
        return evidence.model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Event not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{event_id}/progression")
def add_progression(event_id: str, request: ProgressionRequest):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        observation = _service.add_progression_observation(
            event_id=event_id,
            **request.model_dump(),
        )
        return observation.model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Event not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{event_id}/progression")
def analyze_progression(event_id: str):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        return _service.analyze_progression(event_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Event not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{event_id}/timeline")
def timeline(event_id: str):
    if _service is None:
        raise HTTPException(status_code=503, detail="Disease event service unavailable")

    try:
        return _service.get_timeline(event_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Event not found") from exc
