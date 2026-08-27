from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from app.validation_ground_truth.schemas.models import ClassificationMetrics


class ClassificationEvaluator:
    """Compute standard classification metrics.

    These metrics are applicable only when the target/prediction values form a
    classification task. The evaluator does not infer class semantics.
    """

    def evaluate(self, y_true: list, y_pred: list) -> ClassificationMetrics:
        if len(y_true) != len(y_pred):
            raise ValueError("LENGTH_MISMATCH")

        if not y_true:
            return ClassificationMetrics(sample_count=0)

        return ClassificationMetrics(
            sample_count=len(y_true),
            accuracy=float(accuracy_score(y_true, y_pred)),
            precision_macro=float(
                precision_score(
                    y_true, y_pred, average="macro", zero_division=0
                )
            ),
            recall_macro=float(
                recall_score(
                    y_true, y_pred, average="macro", zero_division=0
                )
            ),
            f1_macro=float(
                f1_score(
                    y_true, y_pred, average="macro", zero_division=0
                )
            ),
        )
