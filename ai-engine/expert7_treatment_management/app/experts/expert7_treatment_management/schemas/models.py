from enum import Enum
from pydantic import BaseModel, Field


class ModelTask(str, Enum):
    CLASSIFICATION = "CLASSIFICATION"
    RANKING = "RANKING"
    RECOMMENDATION = "RECOMMENDATION"


class TreatmentManagementRequest(BaseModel):
    case_id: str
    input_path: str
    model_version: str = "production"


class TreatmentCandidate(BaseModel):
    treatment_id: str
    treatment_type: str
    priority: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)
    validation_required: bool = True


class TreatmentManagementResult(BaseModel):
    expert: str = "EXPERT_7_TREATMENT_MANAGEMENT"
    case_id: str
    model_name: str
    model_version: str
    task: ModelTask
    treatments: list[TreatmentCandidate] = Field(default_factory=list)
    processing_time_ms: float = Field(ge=0.0)
    evidence_quality: str
    status: str
    error_code: str | None = None
    error_message: str | None = None
