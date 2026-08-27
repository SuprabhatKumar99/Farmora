from app.followup_feedback.schemas.models import LearningCandidate


class ModelFeedbackCandidateBuilder:
    """Create reviewable model-improvement candidates.

    This component does not retrain or modify model weights automatically.
    """

    def build(
        self,
        case_id: str,
        feedback,
        original_model_name: str,
        original_model_version: str,
    ) -> list[LearningCandidate]:
        candidates = []

        for item in feedback:
            if not item.verified:
                continue

            candidates.append(
                LearningCandidate(
                    case_id=case_id,
                    candidate_type="MODEL_FEEDBACK_CANDIDATE",
                    source_feedback_ids=[item.feedback_id],
                    status="CANDIDATE",
                    requires_review=True,
                    payload={
                        "model_name": original_model_name,
                        "model_version": original_model_version,
                        "feedback_type": item.feedback_type.value,
                        "observation": item.observation,
                    },
                )
            )

        return candidates
