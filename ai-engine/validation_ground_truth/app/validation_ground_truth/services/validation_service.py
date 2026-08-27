from app.validation_ground_truth.metrics.classification import (
    ClassificationEvaluator,
)
from app.validation_ground_truth.traceability.tracer import ValidationTracer
from app.validation_ground_truth.validation.validator import (
    GroundTruthValidator,
)
from app.validation_ground_truth.schemas.models import (
    ValidationRequest,
    ValidationResult,
)


class ValidationGroundTruthService:
    """Compare a model output with verified ground truth where a declared
    classification target is available.

    It does not manufacture labels or silently treat unverified records as
    ground truth.
    """

    def __init__(self):
        self.validator = GroundTruthValidator()
        self.evaluator = ClassificationEvaluator()
        self.tracer = ValidationTracer()

    def validate(self, request: ValidationRequest) -> ValidationResult:
        gt = request.ground_truth

        if not self.validator.is_usable_for_validation(gt):
            return ValidationResult(
                case_id=request.case_id,
                valid_ground_truth=False,
                ground_truth_status=gt.status,
                status="GROUND_TRUTH_NOT_USABLE",
                traceability=self.tracer.build(gt, request.prediction),
            )

        mismatches = []
        metrics = None

        # Explicit classification contract:
        # ground_truth = {"label": "..."} and prediction = {"label": "..."}.
        # No field is guessed if it is absent.
        true_label = gt.ground_truth.get("label")
        pred_label = request.prediction.get("label")

        if true_label is not None and pred_label is not None:
            metrics = self.evaluator.evaluate(
                [true_label],
                [pred_label],
            )
            if true_label != pred_label:
                mismatches.append({
                    "field": "label",
                    "ground_truth": true_label,
                    "prediction": pred_label,
                })
        else:
            return ValidationResult(
                case_id=request.case_id,
                valid_ground_truth=True,
                ground_truth_status=gt.status,
                status="NO_COMPATIBLE_CLASSIFICATION_TARGET",
                traceability=self.tracer.build(gt, request.prediction),
            )

        return ValidationResult(
            case_id=request.case_id,
            valid_ground_truth=True,
            ground_truth_status=gt.status,
            metrics=metrics,
            mismatches=mismatches,
            traceability=self.tracer.build(gt, request.prediction),
            status="VALIDATED",
        )
