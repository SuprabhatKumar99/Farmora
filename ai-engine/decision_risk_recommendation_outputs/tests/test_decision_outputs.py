from app.decision_outputs.schemas.models import (
    DecisionOutputInput,
    DecisionOutputRequest,
)
from app.decision_outputs.services.output_service import (
    DecisionRiskRecommendationService,
)


def test_unknown_risk_and_validation_when_risk_missing():
    decision = DecisionOutputInput(
        diagnosis="TEST_ONLY",
        confidence=0.8,
        expert_or_lab_validation_required=True,
        reasoning_evidence_ids=["E1"],
    )

    result = DecisionRiskRecommendationService().build(
        DecisionOutputRequest(
            case_id="CASE-1",
            decision=decision,
            model_name="fake",
            model_version="test-1",
        )
    )

    assert result.risk.level.value == "UNKNOWN"
    assert result.validation_required is True
    assert result.evidence_ids == ["E1"]
    assert len(result.recommendations) == 1
    assert result.recommendations[0].type.value == "VALIDATION"


def test_known_risk_is_preserved():
    decision = DecisionOutputInput(
        diagnosis="TEST_ONLY",
        disease_pest_risk="high",
        confidence=0.9,
        prevention=["TEST PREVENTION"],
        reasoning_evidence_ids=["E1", "E2"],
        expert_or_lab_validation_required=True,
    )

    result = DecisionRiskRecommendationService().build(
        DecisionOutputRequest(
            case_id="CASE-2",
            decision=decision,
            model_name="fake",
            model_version="test-2",
        )
    )

    assert result.risk.level.value == "HIGH"
    assert result.recommendations[0].type.value == "PREVENTION"
    assert result.recommendations[0].source_evidence_ids == ["E1", "E2"]


def test_duplicate_evidence_ids_are_removed():
    decision = DecisionOutputInput(
        reasoning_evidence_ids=["E1", "E1", "E2"]
    )

    result = DecisionRiskRecommendationService().build(
        DecisionOutputRequest(
            case_id="CASE-3",
            decision=decision,
        )
    )

    assert result.evidence_ids == ["E1", "E2"]
