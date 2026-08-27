from typing import Any
from pydantic import BaseModel, Field

class Crop(BaseModel):
    crop_id: str
    crop_name: str
    scientific_name: str | None = None
    family: str | None = None
    lifecycle: str | None = None

class Variety(BaseModel):
    variety_id: str
    crop_id: str
    variety_name: str
    maturity_days: int | None = Field(default=None, ge=0)
    disease_susceptibility: str | None = None

class GrowthStage(BaseModel):
    stage_id: str
    crop_id: str
    stage_name: str
    start_day: int | None = Field(default=None, ge=0)
    end_day: int | None = Field(default=None, ge=0)
    expected_features: str | None = None

class CropRequirement(BaseModel):
    crop_id: str
    variety_id: str | None = None
    temperature_min: float | None = None
    temperature_max: float | None = None
    humidity_min: float | None = None
    humidity_max: float | None = None
    soil_moisture_min: float | None = None
    soil_moisture_max: float | None = None

class CropContext(BaseModel):
    crop: dict[str, Any]
    varieties: list[dict[str, Any]]
    growth_stages: list[dict[str, Any]]
    crop_lifecycle: list[dict[str, Any]]
    requirements: list[dict[str, Any]]
