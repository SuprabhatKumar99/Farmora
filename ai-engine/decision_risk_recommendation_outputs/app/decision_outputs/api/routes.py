from fastapi import APIRouter

from app.decision_outputs.schemas.models import DecisionOutputRequest
from app.decision_outputs.services.output_service import (
    DecisionRiskRecommendationService,
)

router = APIRouter(
    prefix="/api/v1/decision-outputs",
    tags=["decision-risk-recommendation-outputs"],
)

service = DecisionRiskRecommendationService()


@router.post("/build")
def build_output(request: DecisionOutputRequest):
    return service.build(request).model_dump(mode="json")


@router.get("/health")
def health():
    return {
        "status": "UP",
        "component": "DECISION_RISK_RECOMMENDATION_OUTPUTS",
    }
