from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    UNKNOWN = "UNKNOWN"


class RecommendationType(str, Enum):
    PREVENTION = "PREVENTION"
    IPM = "IPM"
    MANAGEMENT = "MANAGEMENT"
    TREATMENT = "TREATMENT"
    MONITORING = "MONITORING"
    VALIDATION = "VALIDATION"


class Recommendation(BaseModel):
    recommendation_id: str
    type: RecommendationType
    action: str
    rationale: str | None = None
    priority: str | None = None
    source_evidence_ids: list[str] = Field(default_factory=list)
    source_model_versions: list[str] = Field(default_factory=list)
    validation_required: bool = True


class DecisionOutputInput(BaseModel):
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


class DecisionOutputRequest(BaseModel):
    case_id: str
    decision: DecisionOutputInput
    evidence_context: dict = Field(default_factory=dict)
    model_name: str = "unknown"
    model_version: str = "unknown"


class RiskAssessment(BaseModel):
    level: RiskLevel
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    basis: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class DecisionRecommendationOutput(BaseModel):
    case_id: str
    diagnosis: str | None
    likely_cause: str | None
    affected_zone: str | None
    risk: RiskAssessment
    recommendations: list[Recommendation]
    validation_required: bool
    evidence_ids: list[str]
    model_name: str
    model_version: str
    status: str
