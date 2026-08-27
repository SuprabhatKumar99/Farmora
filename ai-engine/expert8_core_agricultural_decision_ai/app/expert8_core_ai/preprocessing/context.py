class DecisionContextPreprocessor:
    """Validate and prepare the structured evidence context for Expert 8.

    This layer does not add facts that are absent from the evidence context.
    """

    def prepare(self, evidence_context: dict) -> dict:
        if not isinstance(evidence_context, dict):
            raise ValueError("INVALID_EVIDENCE_CONTEXT")

        required = {
            "evidence",
            "confidence_summary",
            "conflicts",
            "missing_evidence",
            "context",
        }

        missing = sorted(required - set(evidence_context))
        if missing:
            raise ValueError(
                f"INCOMPLETE_EVIDENCE_CONTEXT: {','.join(missing)}"
            )

        return evidence_context
