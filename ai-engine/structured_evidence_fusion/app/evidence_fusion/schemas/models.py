from enum import Enum
from pydantic import BaseModel, Field

class EvidenceType(str, Enum):
    VISUAL_HEALTH="VISUAL_HEALTH"
    CHEMICAL_PESTICIDE_DAMAGE="CHEMICAL_PESTICIDE_DAMAGE"
    ROOT_INTERNAL_HEALTH="ROOT_INTERNAL_HEALTH"
    WHOLE_CROP_HEALTH="WHOLE_CROP_HEALTH"
    ENVIRONMENT_WEATHER="ENVIRONMENT_WEATHER"
    PREVENTION_IPM="PREVENTION_IPM"
    TREATMENT_MANAGEMENT="TREATMENT_MANAGEMENT"

class EvidenceItem(BaseModel):
    evidence_id: str
    expert: str
    evidence_type: EvidenceType
    finding: str
    confidence: float = Field(ge=0.0, le=1.0)
    severity: float | None = Field(default=None, ge=0.0, le=1.0)
    affected_zone: str | None = None
    source_ids: list[str] = Field(default_factory=list)
    model_name: str | None = None
    model_version: str | None = None
    attributes: dict = Field(default_factory=dict)

class EvidenceFusionRequest(BaseModel):
    case_id: str
    evidences: list[EvidenceItem] = Field(default_factory=list)

class EvidenceConflict(BaseModel):
    conflict_id: str
    evidence_ids: list[str]
    conflict_type: str
    description: str

class MissingEvidence(BaseModel):
    evidence_type: str
    reason: str

class FusedEvidenceContext(BaseModel):
    case_id: str
    evidence: list[EvidenceItem]
    confidence_summary: dict
    conflicts: list[EvidenceConflict]
    missing_evidence: list[MissingEvidence]
    context: dict
    status: str
