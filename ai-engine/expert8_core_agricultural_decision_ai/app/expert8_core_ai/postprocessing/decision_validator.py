from app.expert8_core_ai.schemas.models import DecisionOutput


class DecisionValidator:
    """Validate structure and apply the safety default for validation."""

    def validate(self, raw: dict) -> DecisionOutput:
        decision = DecisionOutput.model_validate(raw)

        # Expert/laboratory validation remains the safe default unless the
        # supplied evidence/model explicitly supports otherwise.
        if "expert_or_lab_validation_required" not in raw:
            decision.expert_or_lab_validation_required = True

        return decision
