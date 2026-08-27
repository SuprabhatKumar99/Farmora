from app.followup_feedback.schemas.models import (
    FeedbackRecord,
    OutcomeComparison,
)


class OutcomeComparator:
    """Compare explicitly supplied original and follow-up fields.

    No improvement, causality, or treatment efficacy is inferred unless the
    corresponding follow-up observation explicitly provides it.
    """

    def compare(
        self,
        case_id: str,
        original: dict,
        feedback: list[FeedbackRecord],
    ) -> OutcomeComparison:
        changes = []
        feedback_ids = []

        for item in feedback:
            feedback_ids.append(item.feedback_id)

            for field, new_value in item.observation.items():
                old_value = original.get(field)
                if old_value != new_value:
                    changes.append({
                        "field": field,
                        "before": old_value,
                        "after": new_value,
                        "feedback_id": item.feedback_id,
                    })

        return OutcomeComparison(
            case_id=case_id,
            comparable=bool(feedback),
            changes=changes,
            supporting_feedback_ids=feedback_ids,
            validation_required=True,
        )
