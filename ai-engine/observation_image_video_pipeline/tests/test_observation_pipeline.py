from pathlib import Path
import cv2
import numpy as np

from app.observation.media.validator import MediaValidator
from app.observation.services.service import ObservationService
from app.observation.storage.local import LocalMediaStorage


def create_image(path: Path):
    image = np.zeros((32, 32, 3), dtype=np.uint8)
    assert cv2.imwrite(str(path), image)


def test_image_validation(tmp_path):
    image = tmp_path / "sample.jpg"
    create_image(image)

    result = MediaValidator().validate(image, "image/jpeg")

    assert result.valid is True
    assert result.media_type.value == "IMAGE"
    assert result.width == 32
    assert result.height == 32


def test_observation_creation(tmp_path):
    image = tmp_path / "sample.jpg"
    create_image(image)

    service = ObservationService(
        storage=LocalMediaStorage(tmp_path / "media"),
        validator=MediaValidator(),
    )

    observation = service.create(
        source_path=image,
        original_filename="sample.jpg",
        content_type="image/jpeg",
    )

    assert observation.observation_id.startswith("OBS-")
    assert observation.status.value == "VALIDATED"
    assert Path(observation.media_path).exists()
