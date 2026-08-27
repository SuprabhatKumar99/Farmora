from fastapi import APIRouter
from app.evidence_fusion.schemas.models import EvidenceFusionRequest
from app.evidence_fusion.services.fusion_service import StructuredEvidenceFusionService

router=APIRouter(prefix="/api/v1/evidence-fusion",tags=["structured-evidence-fusion"])
service=StructuredEvidenceFusionService()

@router.post("/fuse")
def fuse(request: EvidenceFusionRequest):
    return service.fuse(request).model_dump(mode="json")

@router.get("/health")
def health():
    return {"status":"UP","component":"STRUCTURED_EVIDENCE_FUSION"}
