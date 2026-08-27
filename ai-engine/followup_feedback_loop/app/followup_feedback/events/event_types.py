from enum import Enum


class FeedbackEventType(str, Enum):
    FOLLOW_UP_CREATED = "followup.created"
    FOLLOW_UP_SCHEDULED = "followup.scheduled"
    FEEDBACK_RECEIVED = "followup.feedback.received"
    OUTCOME_RECORDED = "followup.outcome.recorded"
    VALIDATION_COMPLETED = "followup.validation.completed"
    LEARNING_CANDIDATE_CREATED = "followup.learning.candidate.created"
