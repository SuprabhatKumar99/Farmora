from fastapi import APIRouter, HTTPException

from app.experts.expert6_prevention_ipm.schemas.models import (
    PreventionIPMRequest,
)
from app.experts.expert6_prevention_ipm.services.service import (
    Expert6PreventionIPMService,
)


router = APIRouter(
    prefix="/api/v1/experts/expert6/prevention-ipm",
    tags=["expert6-prevention-ipm"],
)

_service = Expert6PreventionIPMService()


@router.post("/analyze")
def analyze(request: PreventionIPMRequest):
    result = _service.analyze(
        case_id=request.case_id,
        input_path=request.input_path,
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
            "message": "No Expert 6 model is loaded.",
        }

    return {
        "loaded": True,
        **_service.model.metadata(),
    }


def get_service():
    return _service
