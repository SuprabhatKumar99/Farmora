from fastapi import APIRouter, HTTPException

from app.experts.expert3_root_internal_health.schemas.models import (
    RootInternalHealthRequest,
)
from app.experts.expert3_root_internal_health.services.service import (
    Expert3RootInternalHealthService,
)


router = APIRouter(
    prefix="/api/v1/experts/expert3/root-internal-health",
    tags=["expert3-root-internal-health"],
)

_service = Expert3RootInternalHealthService()


@router.post("/analyze")
def analyze(request: RootInternalHealthRequest):
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
            "message": "No Expert 3 model is loaded.",
        }

    return {
        "loaded": True,
        **_service.model.metadata(),
    }


def get_service():
    return _service
