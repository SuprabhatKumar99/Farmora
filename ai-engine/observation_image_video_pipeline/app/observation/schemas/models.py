from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ObservationType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class ObservationStatus(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ObservationMetadata(BaseModel):
    farm_id: str | None = None
    zone_id: str | None = None
    crop_id: str | None = None
    variety_id: str | None = None
    captured_at: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    source: str | None = None


class Observation(BaseModel):
    observation_id: str
    observation_type: ObservationType
    status: ObservationStatus
    original_filename: str
    media_path: str
    content_type: str
    size_bytes: int = Field(ge=0)
    metadata: ObservationMetadata = Field(default_factory=ObservationMetadata)
    created_at: datetime


class MediaValidationResult(BaseModel):
    valid: bool
    media_type: ObservationType | None = None
    content_type: str
    size_bytes: int
    width: int | None = None
    height: int | None = None
    frame_count: int | None = None
    fps: float | None = None
    duration_seconds: float | None = None
    error_code: str | None = None
    error_message: str | None = None
