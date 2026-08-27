class EvidenceGuard:
    """Prevent Expert 8 from being invoked without fusion output."""

    def check(self, context: dict):
        if not context.get("evidence") and not context.get("missing_evidence"):
            raise ValueError("NO_EVIDENCE_CONTEXT")

        return True
