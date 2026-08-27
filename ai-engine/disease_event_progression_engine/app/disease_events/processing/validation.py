from datetime import timezone


class DiseaseEventValidator:
    """Validates event temporal consistency and references."""

    def validate_event(self, event):
        if event.last_observed_at < event.first_observed_at:
            raise ValueError(
                "last_observed_at cannot be earlier than first_observed_at"
            )

        if event.updated_at < event.created_at:
            raise ValueError(
                "updated_at cannot be earlier than created_at"
            )

        if event.updated_at.tzinfo is None:
            event.updated_at = event.updated_at.replace(tzinfo=timezone.utc)

        return event

    def validate_progression(self, event, observation):
        if observation.event_id != event.event_id:
            raise ValueError("Progression observation belongs to another event.")

        if observation.observed_at < event.first_observed_at:
            raise ValueError(
                "Progression observation cannot precede first_observed_at."
            )

        if observation.observed_at > event.last_observed_at:
            raise ValueError(
                "Progression observation cannot be later than last_observed_at."
            )

        return observation

    def validate_evidence(self, event, evidence):
        if evidence.event_id != event.event_id:
            raise ValueError("Evidence belongs to another event.")

        if evidence.observed_at < event.first_observed_at:
            raise ValueError(
                "Evidence cannot precede first_observed_at."
            )

        if evidence.observed_at > event.last_observed_at:
            raise ValueError(
                "Evidence cannot be later than last_observed_at."
            )

        return evidence
