from fastapi import APIRouter

from app.validation_ground_truth.schemas.models import (
    ValidationRequest,
)
from app.validation_ground_truth.services.validation_service import (
    ValidationGroundTruthService,
)

router = APIRouter(
    prefix="/api/v1/validation-ground-truth",
    tags=["validation-ground-truth"],
)

service = ValidationGroundTruthService()


@router.post("/validate")
def validate(request: ValidationRequest):
    return service.validate(request).model_dump(mode="json")


@router.get("/health")
def health():
    return {
        "status": "UP",
        "component": "VALIDATION_GROUND_TRUTH",
    }
