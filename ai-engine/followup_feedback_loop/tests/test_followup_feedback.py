from app.followup_feedback.schemas.models import (
    FeedbackRecord,
    FeedbackType,
    FollowUpCase,
)
from app.followup_feedback.services.followup_service import (
    FollowUpFeedbackService,
)


def make_case():
    return FollowUpCase(
        case_id="CASE-1",
        original_decision_id="DEC-1",
        original_model_name="expert8-test",
        original_model_version="1.0",
        created_at="2026-08-27T00:00:00Z",
        original_evidence_ids=["E1"],
        original_recommendation_ids=["R1"],
    )


def test_followup_case_and_feedback():
    service = FollowUpFeedbackService()
    service.create_case(make_case())

    feedback = FeedbackRecord(
        feedback_id="F1",
        case_id="CASE-1",
        feedback_type=FeedbackType.FIELD_OBSERVATION,
        observed_at="2026-08-28T00:00:00Z",
        source_id="FIELD-1",
        observation={"severity": "lower"},
        verified=False,
    )

    service.add_feedback("CASE-1", feedback)

    result = service.compare(
        "CASE-1",
        {"severity": "high"},
    )

    assert result["comparison"].comparable is True
    assert result["comparison"].changes[0]["field"] == "severity"
    assert result["comparison"].validation_required is True


def test_unverified_feedback_does_not_create_learning_candidate():
    service = FollowUpFeedbackService()
    service.create_case(make_case())

    feedback = FeedbackRecord(
        feedback_id="F1",
        case_id="CASE-1",
        feedback_type=FeedbackType.FIELD_OBSERVATION,
        observed_at="2026-08-28T00:00:00Z",
        observation={"severity": "lower"},
        verified=False,
    )
    service.add_feedback("CASE-1", feedback)

    candidates = service.build_learning_candidates("CASE-1")

    assert candidates["knowledge_candidates"] == []
    assert candidates["model_feedback_candidates"] == []


def test_verified_feedback_creates_reviewable_candidates():
    service = FollowUpFeedbackService()
    service.create_case(make_case())

    feedback = FeedbackRecord(
        feedback_id="F1",
        case_id="CASE-1",
        feedback_type=FeedbackType.LAB_RESULT,
        observed_at="2026-08-28T00:00:00Z",
        source_id="LAB-1",
        observation={"result": "example"},
        verified=True,
        reviewer_ids=["reviewer-1"],
    )
    service.add_feedback("CASE-1", feedback)

    candidates = service.build_learning_candidates("CASE-1")

    assert len(candidates["knowledge_candidates"]) == 1
    assert len(candidates["model_feedback_candidates"]) == 1
    assert candidates["knowledge_candidates"][0]["requires_review"] is True
