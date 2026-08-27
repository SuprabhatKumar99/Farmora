from app.followup_feedback.cases.case_manager import FollowUpCaseManager
from app.followup_feedback.comparison.outcome_comparator import OutcomeComparator
from app.followup_feedback.knowledge_update.candidate_builder import (
    KnowledgeUpdateCandidateBuilder,
)
from app.followup_feedback.model_feedback.candidate_builder import (
    ModelFeedbackCandidateBuilder,
)
from app.followup_feedback.schemas.models import (
    FeedbackRecord,
    FollowUpCase,
    FollowUpStatus,
)
from app.followup_feedback.traceability.tracer import FollowUpTracer


class FollowUpFeedbackService:
    def __init__(self):
        self.case_manager = FollowUpCaseManager()
        self.comparator = OutcomeComparator()
        self.knowledge_candidates = KnowledgeUpdateCandidateBuilder()
        self.model_candidates = ModelFeedbackCandidateBuilder()
        self.tracer = FollowUpTracer()
        self.feedback_store = {}

    def create_case(self, case: FollowUpCase):
        if case.case_id in self.feedback_store:
            raise ValueError("FOLLOWUP_CASE_ALREADY_EXISTS")

        self.feedback_store[case.case_id] = {
            "case": case,
            "feedback": [],
        }
        return case

    def add_feedback(self, case_id: str, feedback: FeedbackRecord):
        if case_id not in self.feedback_store:
            raise ValueError("FOLLOWUP_CASE_NOT_FOUND")

        record = self.feedback_store[case_id]
        record["feedback"].append(feedback)
        record["case"].feedback_ids.append(feedback.feedback_id)

        self.case_manager.transition(
            record["case"],
            FollowUpStatus.OBSERVATION_RECEIVED,
        )

        return feedback

    def compare(
        self,
        case_id: str,
        original_decision: dict,
    ):
        if case_id not in self.feedback_store:
            raise ValueError("FOLLOWUP_CASE_NOT_FOUND")

        record = self.feedback_store[case_id]
        feedback = record["feedback"]

        comparison = self.comparator.compare(
            case_id,
            original_decision,
            feedback,
        )

        return {
            "comparison": comparison,
            "traceability": self.tracer.build(
                record["case"],
                feedback,
                comparison,
            ),
        }

    def build_learning_candidates(self, case_id: str):
        if case_id not in self.feedback_store:
            raise ValueError("FOLLOWUP_CASE_NOT_FOUND")

        record = self.feedback_store[case_id]
        case = record["case"]
        feedback = record["feedback"]

        evidence_ids = list(case.original_evidence_ids)

        return {
            "knowledge_candidates": [
                item.model_dump(mode="json")
                for item in self.knowledge_candidates.build(
                    case_id,
                    feedback,
                    evidence_ids,
                )
            ],
            "model_feedback_candidates": [
                item.model_dump(mode="json")
                for item in self.model_candidates.build(
                    case_id,
                    feedback,
                    case.original_model_name,
                    case.original_model_version,
                )
            ],
        }
