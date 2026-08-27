from app.decision_outputs.schemas.models import (
    DecisionOutputInput,
    DecisionRecommendationOutput,
)


class DecisionOutputValidator:
    """Validate that Step 17 contains traceable, structured output."""

    def validate(
        self,
        result: DecisionRecommendationOutput,
        decision: DecisionOutputInput,
    ) -> DecisionRecommendationOutput:
        if decision.expert_or_lab_validation_required:
            result.validation_required = True

        if not result.evidence_ids:
            result.validation_required = True

        return result
