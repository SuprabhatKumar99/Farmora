from datetime import datetime, timezone

from app.environment.processing.quality import SensorQualityProcessor
from app.environment.schemas.models import Sensor, SensorType
from app.environment.services.service import EnvironmentSensorService
from app.environment.storage.in_memory import InMemorySensorStore


def make_service():
    return EnvironmentSensorService(InMemorySensorStore())


def test_register_sensor():
    service = make_service()

    sensor = Sensor(
        sensor_id="S001",
        farm_id="F001",
        zone_id="Z001",
        sensor_type=SensorType.SOIL_MOISTURE,
        unit="%",
    )

    saved = service.register_sensor(sensor)

    assert saved.sensor_id == "S001"


def test_valid_reading_is_accepted():
    service = make_service()

    service.register_sensor(
        Sensor(
            sensor_id="S001",
            farm_id="F001",
            zone_id="Z001",
            sensor_type=SensorType.SOIL_MOISTURE,
            unit="%",
        )
    )

    reading = service.ingest_reading(
        sensor_id="S001",
        value=45.0,
        recorded_at=datetime.now(timezone.utc),
    )

    assert reading.status.value == "ACCEPTED"
    assert reading.value == 45.0


def test_implausible_reading_is_rejected():
    service = make_service()

    service.register_sensor(
        Sensor(
            sensor_id="S001",
            farm_id="F001",
            zone_id="Z001",
            sensor_type=SensorType.SOIL_MOISTURE,
            unit="%",
        )
    )

    reading = service.ingest_reading(
        sensor_id="S001",
        value=150.0,
        recorded_at=datetime.now(timezone.utc),
    )

    assert reading.status.value == "REJECTED"


def test_quality_processor():
    processor = SensorQualityProcessor()

    result = processor.validate(
        SensorType.HUMIDITY,
        60.0,
        datetime.now(timezone.utc),
    )

    assert result.accepted is True
    assert result.normalized_value == 60.0


def test_unknown_sensor():
    service = make_service()

    try:
        service.ingest_reading(
            "UNKNOWN",
            10.0,
            datetime.now(timezone.utc),
        )
    except ValueError as exc:
        assert "Unknown sensor_id" in str(exc)
        return

    raise AssertionError("Expected ValueError")
