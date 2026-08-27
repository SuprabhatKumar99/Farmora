from app.validation_ground_truth.schemas.models import (
    GroundTruthRecord,
    GroundTruthStatus,
    ValidationRequest,
)
from app.validation_ground_truth.services.validation_service import (
    ValidationGroundTruthService,
)


def verified(label):
    return GroundTruthRecord(
        case_id="CASE-1",
        target_type="classification",
        ground_truth={"label": label},
        status=GroundTruthStatus.VERIFIED,
        reviewer_ids=["reviewer-1"],
        source_ids=["source-1"],
    )


def test_verified_matching_prediction():
    result = ValidationGroundTruthService().validate(
        ValidationRequest(
            case_id="CASE-1",
            prediction={"label": "A"},
            ground_truth=verified("A"),
        )
    )
    assert result.status == "VALIDATED"
    assert result.metrics.accuracy == 1.0
    assert result.mismatches == []


def test_verified_mismatch():
    result = ValidationGroundTruthService().validate(
        ValidationRequest(
            case_id="CASE-1",
            prediction={"label": "B"},
            ground_truth=verified("A"),
        )
    )
    assert result.status == "VALIDATED"
    assert result.metrics.accuracy == 0.0
    assert len(result.mismatches) == 1


def test_unverified_is_not_ground_truth():
    record = GroundTruthRecord(
        case_id="CASE-1",
        target_type="classification",
        ground_truth={"label": "A"},
        status=GroundTruthStatus.DRAFT,
    )
    result = ValidationGroundTruthService().validate(
        ValidationRequest(
            case_id="CASE-1",
            prediction={"label": "A"},
            ground_truth=record,
        )
    )
    assert result.valid_ground_truth is False
    assert result.status == "GROUND_TRUTH_NOT_USABLE"


def test_no_compatible_target_is_not_fabricated():
    result = ValidationGroundTruthService().validate(
        ValidationRequest(
            case_id="CASE-1",
            prediction={"diagnosis": "A"},
            ground_truth=verified("A"),
        )
    )
    assert result.status == "NO_COMPATIBLE_CLASSIFICATION_TARGET"
