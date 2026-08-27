from pathlib import Path
import cv2
import numpy as np
from app.experts.expert1_visual_health.preprocessing.image import ImagePreprocessor
from app.experts.expert1_visual_health.services.service import Expert1VisualHealthService

class FakeVisualModel:
    name = "fake-expert1"
    version = "test-1"
    task = "DETECTION"
    def predict(self, image, confidence_threshold):
        return [{"class_id": 1, "class_name": "visual_anomaly",
                 "confidence": 0.92, "bbox": [2,3,20,21]}]

def create_image(path: Path):
    image = np.zeros((64,64,3), dtype=np.uint8)
    assert cv2.imwrite(str(path), image)

def test_preprocessor_loads_image(tmp_path):
    p = tmp_path / "sample.jpg"
    create_image(p)
    image = ImagePreprocessor().load(p)
    assert image.shape == (64,64,3)

def test_service_with_test_model(tmp_path):
    p = tmp_path / "sample.jpg"
    create_image(p)
    result = Expert1VisualHealthService(FakeVisualModel()).analyze(
        "OBS-001", str(p), 0.25
    )
    assert result.status == "COMPLETED"
    assert result.expert == "EXPERT_1_VISUAL_HEALTH"
    assert result.model_version == "test-1"
    assert len(result.detections) == 1

def test_missing_model(tmp_path):
    p = tmp_path / "sample.jpg"
    create_image(p)
    result = Expert1VisualHealthService().analyze("OBS-001", str(p))
    assert result.status == "FAILED"
    assert result.error_code == "MODEL_NOT_LOADED"
