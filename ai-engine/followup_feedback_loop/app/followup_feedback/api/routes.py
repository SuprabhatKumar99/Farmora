from fastapi import APIRouter, HTTPException

from app.followup_feedback.schemas.models import (
    FeedbackRecord,
    FollowUpCase,
)
from app.followup_feedback.services.followup_service import (
    FollowUpFeedbackService,
)

router = APIRouter(
    prefix="/api/v1/followup-feedback",
    tags=["followup-feedback"],
)

service = FollowUpFeedbackService()


@router.post("/cases")
def create_case(case: FollowUpCase):
    try:
        return service.create_case(case).model_dump(mode="json")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.post("/cases/{case_id}/feedback")
def add_feedback(case_id: str, feedback: FeedbackRecord):
    try:
        return service.add_feedback(case_id, feedback).model_dump(
            mode="json"
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/cases/{case_id}/compare")
def compare(case_id: str, original_decision: dict):
    try:
        result = service.compare(case_id, original_decision)
        return {
            "comparison": result["comparison"].model_dump(mode="json"),
            "traceability": result["traceability"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/cases/{case_id}/learning-candidates")
def learning_candidates(case_id: str):
    try:
        return service.build_learning_candidates(case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/health")
def health():
    return {
        "status": "UP",
        "component": "FOLLOWUP_FEEDBACK_LOOP",
    }
