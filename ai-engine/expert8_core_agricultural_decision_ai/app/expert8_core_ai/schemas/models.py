from enum import Enum
from pydantic import BaseModel, Field


class DecisionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    NEED_MORE_DATA = "NEED_MORE_DATA"
    VALIDATION_REQUIRED = "VALIDATION_REQUIRED"
    FAILED = "FAILED"


class DecisionRequest(BaseModel):
    case_id: str
    evidence_context: dict
    model_version: str = "production"


class DecisionOutput(BaseModel):
    diagnosis: str | None = None
    likely_cause: str | None = None
    disease_pest_risk: str | None = None
    severity: str | None = None
    affected_zone: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    prevention: list[str] = Field(default_factory=list)
    management: list[str] = Field(default_factory=list)
    treatment_recommendation: list[str] = Field(default_factory=list)
    expert_or_lab_validation_required: bool = True
    reasoning_evidence_ids: list[str] = Field(default_factory=list)


class DecisionResult(BaseModel):
    expert: str = "EXPERT_8_CORE_AGRICULTURAL_DECISION_AI"
    case_id: str
    model_name: str
    model_version: str
    status: DecisionStatus
    decision: DecisionOutput | None = None
    processing_time_ms: float = Field(ge=0.0)
    error_code: str | None = None
    error_message: str | None = None
