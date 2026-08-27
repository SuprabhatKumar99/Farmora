from fastapi import APIRouter, HTTPException

from app.experts.expert7_treatment_management.schemas.models import (
    TreatmentManagementRequest,
)
from app.experts.expert7_treatment_management.services.service import (
    Expert7TreatmentManagementService,
)


router = APIRouter(
    prefix="/api/v1/experts/expert7/treatment-management",
    tags=["expert7-treatment-management"],
)

_service = Expert7TreatmentManagementService()


@router.post("/analyze")
def analyze(request: TreatmentManagementRequest):
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
            "message": "No Expert 7 model is loaded.",
        }

    return {
        "loaded": True,
        **_service.model.metadata(),
    }


def get_service():
    return _service
