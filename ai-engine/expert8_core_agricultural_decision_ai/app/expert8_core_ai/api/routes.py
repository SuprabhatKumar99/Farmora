from fastapi import APIRouter, HTTPException

from app.expert8_core_ai.schemas.models import DecisionRequest
from app.expert8_core_ai.services.decision_service import Expert8DecisionService


router = APIRouter(
    prefix="/api/v1/expert8/core-ai",
    tags=["expert8-core-ai"],
)

service = Expert8DecisionService()


@router.post("/decide")
def decide(request: DecisionRequest):
    result = service.decide(
        case_id=request.case_id,
        evidence_context=request.evidence_context,
    )

    if result.status == "FAILED":
        raise HTTPException(
            status_code=400,
            detail=result.model_dump(mode="json"),
        )

    return result.model_dump(mode="json")


@router.get("/model")
def model_info():
    if service.model is None:
        return {
            "loaded": False,
            "message": "No Expert 8 model is loaded.",
        }

    return {
        "loaded": True,
        **service.model.metadata(),
    }
