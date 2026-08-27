from enum import Enum
from pydantic import BaseModel, Field

class ModelTask(str, Enum):
    CLASSIFICATION = "CLASSIFICATION"
    DETECTION = "DETECTION"
    SEGMENTATION = "SEGMENTATION"

class VisualHealthRequest(BaseModel):
    observation_id: str
    image_path: str
    model_version: str = "production"
    confidence_threshold: float = Field(default=0.25, ge=0.0, le=1.0)

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class VisualDetection(BaseModel):
    class_id: int
    class_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: BoundingBox | None = None

class VisualHealthResult(BaseModel):
    expert: str = "EXPERT_1_VISUAL_HEALTH"
    observation_id: str
    model_name: str
    model_version: str
    task: ModelTask
    detections: list[VisualDetection] = Field(default_factory=list)
    processing_time_ms: float = Field(ge=0.0)
    evidence_quality: str
    status: str
    error_code: str | None = None
    error_message: str | None = None
