from datetime import datetime, timezone

from app.disease_events.schemas.models import ProgressionResult


class DiseaseProgressionEngine:
    """Computes descriptive temporal progression from severity observations.

    It does not infer disease identity or prescribe treatment.
    """

    @staticmethod
    def _hours_between(start: datetime, end: datetime) -> float:
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)

        return (end - start).total_seconds() / 3600.0

    def analyze(self, event_id: str, observations) -> ProgressionResult:
        if not observations:
            raise ValueError("At least one progression observation is required.")

        ordered = sorted(
            observations,
            key=lambda item: item.observed_at,
        )

        first = ordered[0]
        last = ordered[-1]

        previous = ordered[-2] if len(ordered) >= 2 else None

        if previous is None:
            change = None
            direction = "INSUFFICIENT_HISTORY"
            elapsed = None
            previous_severity = None
        else:
            change = last.severity - previous.severity
            elapsed = self._hours_between(
                previous.observed_at,
                last.observed_at,
            )
            previous_severity = previous.severity

            if change > 0:
                direction = "INCREASING"
            elif change < 0:
                direction = "DECREASING"
            else:
                direction = "STABLE"

        return ProgressionResult(
            event_id=event_id,
            previous_severity=previous_severity,
            current_severity=last.severity,
            severity_change=change,
            elapsed_hours=elapsed,
            direction=direction,
            observation_count=len(ordered),
            first_observed_at=first.observed_at,
            last_observed_at=last.observed_at,
        )
