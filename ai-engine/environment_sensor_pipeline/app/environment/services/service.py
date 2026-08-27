from datetime import datetime, timezone
from uuid import uuid4

from app.environment.processing.quality import SensorQualityProcessor
from app.environment.schemas.models import (
    ReadingStatus,
    Sensor,
    SensorReading,
)


class EnvironmentSensorService:
    def __init__(self, store, quality_processor=None):
        self.store = store
        self.quality = quality_processor or SensorQualityProcessor()

    def register_sensor(self, sensor: Sensor):
        self.store.save_sensor(sensor)
        return sensor

    def ingest_reading(
        self,
        sensor_id: str,
        value: float,
        recorded_at: datetime,
    ) -> SensorReading:
        sensor = self.store.get_sensor(sensor_id)

        if sensor is None:
            raise ValueError(f"Unknown sensor_id: {sensor_id}")

        quality = self.quality.validate(
            sensor.sensor_type,
            value,
            recorded_at,
        )

        status = (
            ReadingStatus.ACCEPTED
            if quality.accepted
            else ReadingStatus.REJECTED
        )

        reading = SensorReading(
            reading_id=f"READ-{uuid4().hex[:12]}",
            sensor_id=sensor.sensor_id,
            farm_id=sensor.farm_id,
            zone_id=sensor.zone_id,
            sensor_type=sensor.sensor_type,
            value=float(value),
            unit=sensor.unit,
            recorded_at=recorded_at,
            received_at=datetime.now(timezone.utc),
            status=status,
        )

        self.store.save_reading(reading)
        return reading

    def list_readings(self):
        return self.store.list_readings()
