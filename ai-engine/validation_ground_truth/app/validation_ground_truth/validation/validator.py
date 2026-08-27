from app.validation_ground_truth.schemas.models import (
    GroundTruthRecord,
    GroundTruthStatus,
)


class GroundTruthValidator:
    """Validate dataset-level ground-truth metadata.

    VERIFIED is required before a record can be treated as a validation
    reference. The service does not decide whether an agricultural label is
    scientifically correct; that requires the project's qualified review
    process and source evidence.
    """

    def validate_record(self, record: GroundTruthRecord) -> bool:
        if not record.case_id.strip():
            return False
        if not record.target_type.strip():
            return False
        if not isinstance(record.ground_truth, dict):
            return False

        if record.status == GroundTruthStatus.VERIFIED:
            return bool(record.reviewer_ids or record.source_ids)

        return True

    def is_usable_for_validation(self, record: GroundTruthRecord) -> bool:
        return (
            self.validate_record(record)
            and record.status == GroundTruthStatus.VERIFIED
        )
