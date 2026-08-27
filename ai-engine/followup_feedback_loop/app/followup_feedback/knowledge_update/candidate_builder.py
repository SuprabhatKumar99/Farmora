from app.followup_feedback.schemas.models import LearningCandidate


class KnowledgeUpdateCandidateBuilder:
    """Create reviewable candidates from verified feedback.

    Candidates are never written directly into the production knowledge base.
    """

    def build(
        self,
        case_id: str,
        feedback,
        evidence_ids: list[str],
    ) -> list[LearningCandidate]:
        candidates = []

        for item in feedback:
            if not item.verified:
                continue

            candidates.append(
                LearningCandidate(
                    case_id=case_id,
                    candidate_type="KNOWLEDGE_UPDATE_CANDIDATE",
                    source_feedback_ids=[item.feedback_id],
                    source_evidence_ids=evidence_ids,
                    status="CANDIDATE",
                    requires_review=True,
                    payload=item.observation,
                )
            )

        return candidates
