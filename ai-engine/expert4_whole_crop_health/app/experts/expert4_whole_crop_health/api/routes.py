from fastapi import APIRouter, HTTPException

from app.experts.expert4_whole_crop_health.schemas.models import (
    WholeCropHealthRequest,
)
from app.experts.expert4_whole_crop_health.services.service import (
    Expert4WholeCropHealthService,
)


router = APIRouter(
    prefix="/api/v1/experts/expert4/whole-crop-health",
    tags=["expert4-whole-crop-health"],
)

_service = Expert4WholeCropHealthService()


@router.post("/analyze")
def analyze(request: WholeCropHealthRequest):
    result = _service.analyze(
        observation_id=request.observation_id,
        image_path=request.image_path,
        confidence_threshold=request.confidence_threshold,
    )

    if result.status == "FAILED":
        raise HTTPException(
            status_code=400,
            detail=result.model_dump(mode="json"),
        )

    return result.model_dump(mode="json")


@router.get("/model")
def model_info():
    if _service.model is None:
        return {
            "loaded": False,
            "message": "No Expert 4 model is loaded.",
        }

    return {
        "loaded": True,
        **_service.model.metadata(),
    }


def get_service():
    return _service
