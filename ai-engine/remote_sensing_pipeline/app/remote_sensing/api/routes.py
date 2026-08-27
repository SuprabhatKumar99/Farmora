from fastapi import APIRouter, HTTPException

from app.remote_sensing.schemas.models import (
    RemoteSensingProductType,
    RemoteSensingSource,
)
from app.remote_sensing.services.service import RemoteSensingService


router = APIRouter(
    prefix="/api/v1/remote-sensing",
    tags=["remote-sensing"],
)

_service: RemoteSensingService | None = None


def configure_service(service):
    global _service
    _service = service


@router.get("/assets/{asset_id}")
def get_asset(asset_id: str):
    if _service is None:
        raise HTTPException(status_code=503, detail="Remote sensing service unavailable")

    try:
        return _service.get_asset(asset_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
