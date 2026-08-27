from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.observation.media.validator import MediaValidator
from app.observation.schemas.models import (
    Observation,
    ObservationMetadata,
    ObservationStatus,
)
from app.observation.storage.local import LocalMediaStorage


class ObservationService:
    def __init__(self, storage: LocalMediaStorage, validator: MediaValidator):
        self.storage = storage
        self.validator = validator
        self._observations: dict[str, Observation] = {}

    def create(
        self,
        source_path: str | Path,
        original_filename: str,
        content_type: str,
        metadata: ObservationMetadata | None = None,
    ) -> Observation:
        observation_id = f"OBS-{uuid4().hex[:12]}"

        validation = self.validator.validate(
            source_path,
            content_type,
        )

        if not validation.valid:
            raise ValueError(
                f"{validation.error_code}: {validation.error_message}"
            )

        media_path = self.storage.save(
            source=source_path,
            observation_id=observation_id,
            filename=original_filename,
        )

        observation = Observation(
            observation_id=observation_id,
            observation_type=validation.media_type,
            status=ObservationStatus.VALIDATED,
            original_filename=original_filename,
            media_path=media_path,
            content_type=content_type,
            size_bytes=validation.size_bytes,
            metadata=metadata or ObservationMetadata(),
            created_at=datetime.now(timezone.utc),
        )

        self._observations[observation_id] = observation
        return observation

    def get(self, observation_id: str) -> Observation:
        observation = self._observations.get(observation_id)

        if observation is None:
            raise KeyError(observation_id)

        return observation

    def update_status(
        self,
        observation_id: str,
        status: ObservationStatus,
    ) -> Observation:
        observation = self.get(observation_id)
        updated = observation.model_copy(update={"status": status})
        self._observations[observation_id] = updated
        return updated
