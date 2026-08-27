from fastapi import APIRouter,HTTPException
from ..schemas.models import EnvironmentWeatherRequest
from ..services.service import Expert5EnvironmentWeatherService
router=APIRouter(prefix='/api/v1/experts/expert5/environment-weather',tags=['expert5-environment-weather'])
_service=Expert5EnvironmentWeatherService()
@router.post('/analyze')
def analyze(r:EnvironmentWeatherRequest):
    x=_service.analyze(r.observation_id,r.data_path)
    if x.status=='FAILED': raise HTTPException(400,detail=x.model_dump(mode='json'))
    return x.model_dump(mode='json')
@router.get('/model')
def model_info(): return {'loaded':_service.model is not None, **(_service.model.metadata() if _service.model else {})}
def get_service(): return _service
