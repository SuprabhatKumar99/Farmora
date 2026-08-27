from app.decision_outputs.schemas.models import RiskAssessment, RiskLevel


class RiskAssessor:
    """Translate an already-produced Expert 8 risk field into a structured
    risk object.

    This component deliberately does not invent a numeric risk score.
    If Expert 8 provides a recognized qualitative level, it is preserved.
    Otherwise risk remains UNKNOWN.
    """

    LEVELS = {
        "low": RiskLevel.LOW,
        "moderate": RiskLevel.MODERATE,
        "medium": RiskLevel.MODERATE,
        "high": RiskLevel.HIGH,
        "very high": RiskLevel.VERY_HIGH,
        "very_high": RiskLevel.VERY_HIGH,
    }

    def assess(self, risk_text: str | None, confidence: float | None,
               evidence_ids: list[str]) -> RiskAssessment:
        if not risk_text:
            return RiskAssessment(
                level=RiskLevel.UNKNOWN,
                confidence=confidence,
                basis=["Risk level was not supplied by Expert 8."],
                evidence_ids=evidence_ids,
            )

        level = self.LEVELS.get(risk_text.strip().lower())
        if level is None:
            return RiskAssessment(
                level=RiskLevel.UNKNOWN,
                confidence=confidence,
                basis=["Risk text was supplied but does not match the defined qualitative levels."],
                evidence_ids=evidence_ids,
            )

        return RiskAssessment(
            level=level,
            confidence=confidence,
            basis=[f"Risk level supplied by Expert 8: {risk_text}."],
            evidence_ids=evidence_ids,
        )
