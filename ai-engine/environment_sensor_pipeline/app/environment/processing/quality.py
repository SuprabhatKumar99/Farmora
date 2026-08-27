from datetime import datetime, timezone

from app.environment.schemas.models import QualityResult, SensorType


# Conservative physical plausibility ranges. These are validation guardrails,
# not agricultural recommendations or disease thresholds.
DEFAULT_RANGES = {
    SensorType.SOIL_MOISTURE: (0.0, 100.0),
    SensorType.TEMPERATURE: (-80.0, 80.0),
    SensorType.HUMIDITY: (0.0, 100.0),
    SensorType.RAINFALL: (0.0, 2000.0),
    SensorType.LIGHT: (0.0, 200000.0),
    SensorType.LEAF_WETNESS: (0.0, 100.0),
}


class SensorQualityProcessor:
    def __init__(self, ranges=None, max_future_seconds=300):
        self.ranges = ranges or DEFAULT_RANGES
        self.max_future_seconds = max_future_seconds

    def validate(
        self,
        sensor_type: SensorType,
        value: float,
        recorded_at: datetime,
    ) -> QualityResult:
        if value != value or value in (float("inf"), float("-inf")):
            return QualityResult(
                accepted=False,
                reason="NON_FINITE_VALUE",
            )

        limits = self.ranges.get(sensor_type)

        if limits is not None:
            lower, upper = limits
            if value < lower or value > upper:
                return QualityResult(
                    accepted=False,
                    reason="VALUE_OUT_OF_PLAUSIBLE_RANGE",
                )

        now = datetime.now(timezone.utc)
        timestamp = recorded_at

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        if (timestamp - now).total_seconds() > self.max_future_seconds:
            return QualityResult(
                accepted=False,
                reason="FUTURE_TIMESTAMP",
            )

        return QualityResult(
            accepted=True,
            normalized_value=float(value),
        )
