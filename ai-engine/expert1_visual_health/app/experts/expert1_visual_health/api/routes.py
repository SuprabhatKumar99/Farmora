from fastapi import APIRouter, HTTPException
from app.experts.expert1_visual_health.schemas.models import VisualHealthRequest
from app.experts.expert1_visual_health.services.service import Expert1VisualHealthService

router = APIRouter(
    prefix="/api/v1/experts/expert1/visual-health",
    tags=["expert1-visual-health"]
)
_service = Expert1VisualHealthService()

@router.post("/analyze")
def analyze(request: VisualHealthRequest):
    result = _service.analyze(
        request.observation_id, request.image_path,
        request.confidence_threshold
    )
    if result.status == "FAILED":
        raise HTTPException(status_code=400, detail=result.model_dump(mode="json"))
    return result.model_dump(mode="json")

@router.get("/model")
def model_info():
    if _service.model is None:
        return {"loaded": False, "message": "No Expert 1 model is loaded."}
    return {"loaded": True, **_service.model.metadata()}

def get_service():
    return _service
