from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DiseaseEventStatus(str, Enum):
    OBSERVED = "OBSERVED"
    SUSPECTED = "SUSPECTED"
    CONFIRMED = "CONFIRMED"
    RESOLVED = "RESOLVED"


class EvidenceType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    SENSOR = "SENSOR"
    REMOTE_SENSING = "REMOTE_SENSING"
    FARMER_REPORT = "FARMER_REPORT"
    LABORATORY = "LABORATORY"
    EXPERT = "EXPERT"


class DiseaseEvent(BaseModel):
    event_id: str
    farm_id: str
    zone_id: str
    crop_id: str | None = None
    variety_id: str | None = None
    disease_id: str | None = None
    pest_id: str | None = None
    status: DiseaseEventStatus
    severity: float | None = Field(default=None, ge=0.0, le=1.0)
    first_observed_at: datetime
    last_observed_at: datetime
    created_at: datetime
    updated_at: datetime


class DiseaseEventEvidence(BaseModel):
    evidence_id: str
    event_id: str
    evidence_type: EvidenceType
    reference_id: str
    observed_at: datetime
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    notes: str | None = None


class ProgressionObservation(BaseModel):
    observation_id: str
    event_id: str
    observed_at: datetime
    severity: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)


class ProgressionResult(BaseModel):
    event_id: str
    previous_severity: float | None
    current_severity: float
    severity_change: float | None
    elapsed_hours: float | None
    direction: str
    observation_count: int
    first_observed_at: datetime
    last_observed_at: datetime


class DiseaseEventTimeline(BaseModel):
    event: DiseaseEvent
    evidence: list[DiseaseEventEvidence] = Field(default_factory=list)
    progression: list[ProgressionObservation] = Field(default_factory=list)
