from enum import Enum
from pydantic import BaseModel, Field


class ModelTask(str, Enum):
    CLASSIFICATION = "CLASSIFICATION"
    RANKING = "RANKING"
    RECOMMENDATION = "RECOMMENDATION"


class PreventionIPMRequest(BaseModel):
    case_id: str
    input_path: str
    model_version: str = "production"


class PreventionAction(BaseModel):
    action_id: str
    action_type: str
    priority: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)


class PreventionIPMResult(BaseModel):
    expert: str = "EXPERT_6_PREVENTION_IPM"
    case_id: str
    model_name: str
    model_version: str
    task: ModelTask
    actions: list[PreventionAction] = Field(default_factory=list)
    processing_time_ms: float = Field(ge=0.0)
    evidence_quality: str
    status: str
    error_code: str | None = None
    error_message: str | None = None
