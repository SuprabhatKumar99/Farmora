class FollowUpTracer:
    def build(self, case, feedback, comparison=None):
        return {
            "case_id": case.case_id,
            "original_decision_id": case.original_decision_id,
            "original_model_name": case.original_model_name,
            "original_model_version": case.original_model_version,
            "original_evidence_ids": list(case.original_evidence_ids),
            "original_recommendation_ids": list(
                case.original_recommendation_ids
            ),
            "feedback_ids": [item.feedback_id for item in feedback],
            "feedback_source_ids": [
                item.source_id for item in feedback if item.source_id
            ],
            "comparison_available": comparison is not None,
        }
