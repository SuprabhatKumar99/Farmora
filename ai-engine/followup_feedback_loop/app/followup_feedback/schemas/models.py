from enum import Enum
from pydantic import BaseModel, Field


class FollowUpStatus(str, Enum):
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    OBSERVATION_RECEIVED = "OBSERVATION_RECEIVED"
    OUTCOME_RECORDED = "OUTCOME_RECORDED"
    VALIDATED = "VALIDATED"
    CLOSED = "CLOSED"


class FeedbackType(str, Enum):
    FOLLOW_UP_OBSERVATION = "FOLLOW_UP_OBSERVATION"
    TREATMENT_OUTCOME = "TREATMENT_OUTCOME"
    FIELD_OBSERVATION = "FIELD_OBSERVATION"
    EXPERT_RESULT = "EXPERT_RESULT"
    LAB_RESULT = "LAB_RESULT"
    CASE_CORRECTION = "CASE_CORRECTION"


class FeedbackRecord(BaseModel):
    feedback_id: str
    case_id: str
    feedback_type: FeedbackType
    observed_at: str
    source_id: str | None = None
    source_type: str | None = None
    observation: dict = Field(default_factory=dict)
    verified: bool = False
    reviewer_ids: list[str] = Field(default_factory=list)
    notes: str | None = None


class FollowUpCase(BaseModel):
    case_id: str
    original_decision_id: str
    original_model_name: str
    original_model_version: str
    created_at: str
    status: FollowUpStatus = FollowUpStatus.CREATED
    follow_up_due_at: str | None = None
    original_evidence_ids: list[str] = Field(default_factory=list)
    original_recommendation_ids: list[str] = Field(default_factory=list)
    feedback_ids: list[str] = Field(default_factory=list)


class OutcomeComparison(BaseModel):
    case_id: str
    comparable: bool
    changes: list[dict] = Field(default_factory=list)
    supporting_feedback_ids: list[str] = Field(default_factory=list)
    validation_required: bool = True


class LearningCandidate(BaseModel):
    case_id: str
    candidate_type: str
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_evidence_ids: list[str] = Field(default_factory=list)
    status: str = "CANDIDATE"
    requires_review: bool = True
    payload: dict = Field(default_factory=dict)
