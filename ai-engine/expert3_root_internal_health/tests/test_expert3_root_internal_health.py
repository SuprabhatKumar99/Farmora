from pathlib import Path

import cv2
import numpy as np

from app.experts.expert3_root_internal_health.preprocessing.image import (
    ImagePreprocessor,
)
from app.experts.expert3_root_internal_health.services.service import (
    Expert3RootInternalHealthService,
)


class FakeRootInternalModel:
    name = "fake-expert3"
    version = "test-1"
    task = "DETECTION"

    def predict(self, image, confidence_threshold):
        return [
            {
                "class_id": 1,
                "class_name": "root_internal_pattern",
                "confidence": 0.90,
                "bbox": [2, 3, 20, 21],
            }
        ]


def create_image(path: Path):
    image = np.zeros((64, 64, 3), dtype=np.uint8)
    assert cv2.imwrite(str(path), image)


def test_preprocessor_loads_image(tmp_path):
    path = tmp_path / "sample.jpg"
    create_image(path)

    image = ImagePreprocessor().load(path)

    assert image.shape == (64, 64, 3)


def test_expert3_service_with_test_model(tmp_path):
    path = tmp_path / "sample.jpg"
    create_image(path)

    service = Expert3RootInternalHealthService(
        model=FakeRootInternalModel()
    )

    result = service.analyze(
        observation_id="OBS-001",
        image_path=str(path),
        confidence_threshold=0.25,
    )

    assert result.status == "COMPLETED"
    assert result.expert == "EXPERT_3_ROOT_INTERNAL_HEALTH"
    assert result.model_version == "test-1"
    assert len(result.detections) == 1


def test_missing_model_is_reported(tmp_path):
    path = tmp_path / "sample.jpg"
    create_image(path)

    service = Expert3RootInternalHealthService()

    result = service.analyze(
        observation_id="OBS-001",
        image_path=str(path),
    )

    assert result.status == "FAILED"
    assert result.error_code == "MODEL_NOT_LOADED"
