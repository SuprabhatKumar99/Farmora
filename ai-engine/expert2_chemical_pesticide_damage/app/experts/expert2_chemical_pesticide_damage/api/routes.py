from fastapi import APIRouter,HTTPException
from ..schemas.models import ChemicalDamageRequest
from ..services.service import Expert2ChemicalDamageService
router=APIRouter(prefix="/api/v1/experts/expert2/chemical-pesticide-damage",tags=["expert2"])
_service=Expert2ChemicalDamageService()
@router.post("/analyze")
def analyze(r:ChemicalDamageRequest):
    x=_service.analyze(r.observation_id,r.image_path,r.confidence_threshold)
    if x.status=="FAILED": raise HTTPException(400,detail=x.model_dump(mode="json"))
    return x.model_dump(mode="json")
@router.get("/model")
def model(): return {"loaded":_service.model is not None}
def get_service(): return _service
