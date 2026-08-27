class TreatmentPredictionAdapter:
    """Normalize raw model output into treatment candidates.

    The adapter expects the supplied model contract to expose:
    treatment_id, treatment_type, priority, evidence_ids, and optionally
    validation_required.
    """

    def adapt(self, raw_predictions):
        results = []

        for item in raw_predictions or []:
            results.append(
                {
                    "treatment_id": str(item["treatment_id"]),
                    "treatment_type": str(item["treatment_type"]),
                    "priority": float(item["priority"]),
                    "evidence_ids": [
                        str(x) for x in item.get("evidence_ids", [])
                    ],
                    "validation_required": bool(
                        item.get("validation_required", True)
                    ),
                }
            )

        return results
