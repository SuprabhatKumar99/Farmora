from pydantic import BaseModel


class Farm(BaseModel):
    farm_id: str
    location: str
    latitude: float
    longitude: float
    area_hectares: float
    soil_type: str


class Field(BaseModel):
    field_id: str
    farm_id: str
    field_name: str | None = None
    area_hectares: float | None = None


class Zone(BaseModel):
    zone_id: str
    farm_id: str
    zone_number: int
    area_m2: float
    latitude: float
    longitude: float


class CropCycle(BaseModel):
    cycle_id: str
    farm_id: str
    zone_id: str
    crop_id: str
    variety_id: str
    sowing_date: str
    expected_harvest_date: str
    current_stage: str


class FarmDigitalProfile(BaseModel):
    farm: dict
    fields: list[dict]
    zones: list[dict]
    crop_cycles: list[dict]
