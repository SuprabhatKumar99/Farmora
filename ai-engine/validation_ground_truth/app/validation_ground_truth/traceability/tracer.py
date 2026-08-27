class ValidationTracer:
    def build(self, record, prediction):
        return {
            "case_id": record.case_id,
            "ground_truth_source_ids": list(record.source_ids),
            "annotator_ids": list(record.annotator_ids),
            "reviewer_ids": list(record.reviewer_ids),
            "ground_truth_status": record.status.value,
            "prediction_evidence_ids": list(
                prediction.get("reasoning_evidence_ids", [])
            ),
            "prediction_model_name": prediction.get("model_name"),
            "prediction_model_version": prediction.get("model_version"),
        }
