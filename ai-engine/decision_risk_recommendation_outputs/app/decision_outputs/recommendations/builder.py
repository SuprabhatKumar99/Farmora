from app.decision_outputs.schemas.models import (
    DecisionOutputInput,
    Recommendation,
    RecommendationType,
)


class RecommendationBuilder:
    """Convert recommendations already produced by Expert 8 into a common
    output contract. It does not generate new agricultural instructions.
    """

    def build(
        self,
        decision: DecisionOutputInput,
        model_version: str,
    ) -> list[Recommendation]:
        recommendations = []
        counter = 1

        def add(items, kind):
            nonlocal counter
            for action in items:
                if not action or not action.strip():
                    continue

                recommendations.append(
                    Recommendation(
                        recommendation_id=f"REC-{counter:04d}",
                        type=kind,
                        action=action.strip(),
                        rationale=None,
                        priority=None,
                        source_evidence_ids=list(
                            decision.reasoning_evidence_ids
                        ),
                        source_model_versions=[model_version],
                        validation_required=True,
                    )
                )
                counter += 1

        add(decision.prevention, RecommendationType.PREVENTION)
        add(decision.management, RecommendationType.MANAGEMENT)
        add(
            decision.treatment_recommendation,
            RecommendationType.TREATMENT,
        )

        if not recommendations:
            recommendations.append(
                Recommendation(
                    recommendation_id=f"REC-{counter:04d}",
                    type=RecommendationType.VALIDATION,
                    action=(
                        "No actionable recommendation was supplied; "
                        "additional evidence or expert/laboratory validation is required."
                    ),
                    rationale="Expert 8 supplied no actionable recommendation.",
                    priority="HIGH",
                    source_evidence_ids=list(
                        decision.reasoning_evidence_ids
                    ),
                    source_model_versions=[model_version],
                    validation_required=True,
                )
            )

        return recommendations
