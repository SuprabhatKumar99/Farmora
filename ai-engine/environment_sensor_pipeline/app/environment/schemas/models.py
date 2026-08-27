from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class SensorType(str, Enum):
    SOIL_MOISTURE = "SOIL_MOISTURE"
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    RAINFALL = "RAINFALL"
    LIGHT = "LIGHT"
    LEAF_WETNESS = "LEAF_WETNESS"
    OTHER = "OTHER"


class ReadingStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class SensorReading(BaseModel):
    reading_id: str
    sensor_id: str
    farm_id: str | None = None
    zone_id: str | None = None
    sensor_type: SensorType
    value: float
    unit: str
    recorded_at: datetime
    received_at: datetime
    status: ReadingStatus = ReadingStatus.ACCEPTED


class Sensor(BaseModel):
    sensor_id: str
    farm_id: str
    zone_id: str | None = None
    sensor_type: SensorType
    unit: str
    latitude: float | None = None
    longitude: float | None = None
    active: bool = True


class EnvironmentObservation(BaseModel):
    observation_id: str
    farm_id: str | None = None
    zone_id: str | None = None
    observed_at: datetime
    readings: list[SensorReading] = Field(default_factory=list)


class QualityResult(BaseModel):
    accepted: bool
    reason: str | None = None
    normalized_value: float | None = None
