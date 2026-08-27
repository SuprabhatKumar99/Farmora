from pathlib import Path
import shutil
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.observation.schemas.models import ObservationMetadata
from app.observation.services.service import ObservationService


router = APIRouter(prefix="/api/v1/observations", tags=["observations"])

_service: ObservationService | None = None


def configure_service(service: ObservationService):
    global _service
    _service = service


@router.post("")
async def create_observation(
    file: UploadFile = File(...),
    farm_id: str | None = Form(default=None),
    zone_id: str | None = Form(default=None),
    crop_id: str | None = Form(default=None),
    variety_id: str | None = Form(default=None),
):
    if _service is None:
        raise HTTPException(status_code=503, detail="Observation service unavailable")

    suffix = Path(file.filename or "").suffix

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temporary_path = Path(tmp.name)

        shutil.copyfileobj(file.file, tmp)

    try:
        metadata = ObservationMetadata(
            farm_id=farm_id,
            zone_id=zone_id,
            crop_id=crop_id,
            variety_id=variety_id,
        )

        observation = _service.create(
            source_path=temporary_path,
            original_filename=file.filename or "upload",
            content_type=file.content_type or "application/octet-stream",
            metadata=metadata,
        )

        return observation.model_dump(mode="json")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    finally:
        temporary_path.unlink(missing_ok=True)


@router.get("/{observation_id}")
def get_observation(observation_id: str):
    if _service is None:
        raise HTTPException(status_code=503, detail="Observation service unavailable")

    try:
        return _service.get(observation_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Observation not found") from exc
