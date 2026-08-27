from typing import Any
from pydantic import BaseModel

class Disease(BaseModel):
    disease_id: str
    disease_name: str
    crop_id: str
    pathogen_type: str | None = None
    pathogen_name: str | None = None
    affected_parts: str | None = None
    typical_stage: str | None = None

class Pest(BaseModel):
    pest_id: str
    pest_name: str
    crop_id: str
    affected_parts: str | None = None
    typical_stage: str | None = None

class Symptom(BaseModel):
    symptom_id: str
    disease_id: str
    crop_id: str
    plant_part: str | None = None
    symptom_type: str | None = None
    color: str | None = None
    pattern: str | None = None
    severity_stage: str | None = None
    description: str | None = None

class DiseasePestContext(BaseModel):
    diseases: list[dict[str, Any]]
    pests: list[dict[str, Any]]
    symptoms: list[dict[str, Any]]
    disease_progression: list[dict[str, Any]]
    disease_conditions: list[dict[str, Any]]
    management: list[dict[str, Any]]
