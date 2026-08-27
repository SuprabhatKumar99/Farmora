from enum import Enum
from pydantic import BaseModel, Field


class GroundTruthStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class ValidationSplit(str, Enum):
    TRAIN = "TRAIN"
    VALIDATION = "VALIDATION"
    TEST = "TEST"


class GroundTruthRecord(BaseModel):
    case_id: str
    target_type: str
    ground_truth: dict
    status: GroundTruthStatus = GroundTruthStatus.DRAFT
    split: ValidationSplit | None = None
    annotator_ids: list[str] = Field(default_factory=list)
    reviewer_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    notes: str | None = None


class ValidationRequest(BaseModel):
    case_id: str
    prediction: dict
    ground_truth: GroundTruthRecord


class ClassificationMetrics(BaseModel):
    sample_count: int
    accuracy: float | None = None
    precision_macro: float | None = None
    recall_macro: float | None = None
    f1_macro: float | None = None


class ValidationResult(BaseModel):
    case_id: str
    valid_ground_truth: bool
    ground_truth_status: GroundTruthStatus
    metrics: ClassificationMetrics | None = None
    mismatches: list[dict] = Field(default_factory=list)
    traceability: dict = Field(default_factory=dict)
    status: str
