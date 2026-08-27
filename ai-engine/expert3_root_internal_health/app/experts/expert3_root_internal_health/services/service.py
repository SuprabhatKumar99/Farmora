import time

from app.experts.expert3_root_internal_health.preprocessing.image import (
    ImagePreprocessor,
)
from app.experts.expert3_root_internal_health.schemas.models import (
    BoundingBox,
    ModelTask,
    RootInternalDetection,
    RootInternalHealthResult,
)


class Expert3RootInternalHealthService:
    """Expert 3 orchestration.

    Produces structured evidence from the supplied root/internal-health model.
    It does not make a final diagnosis or treatment recommendation.
    """

    def __init__(self, model=None, preprocessor=None):
        self.model = model
        self.preprocessor = preprocessor or ImagePreprocessor()

    def set_model(self, model):
        self.model = model

    def analyze(
        self,
        observation_id: str,
        image_path: str,
        confidence_threshold: float = 0.25,
    ) -> RootInternalHealthResult:
        started = time.perf_counter()

        if self.model is None:
            return self._error(
                observation_id,
                "MODEL_NOT_LOADED",
                "Expert 3 model is not loaded.",
                started,
            )

        try:
            image = self.preprocessor.load(image_path)
            quality = self.preprocessor.quality(image)

            raw = self.model.predict(
                image=image,
                confidence_threshold=confidence_threshold,
            )

            detections = []

            for item in raw or []:
                bbox = item.get("bbox")

                detections.append(
                    RootInternalDetection(
                        class_id=int(item["class_id"]),
                        class_name=str(item["class_name"]),
                        confidence=float(item["confidence"]),
                        bbox=(
                            BoundingBox(
                                x1=float(bbox[0]),
                                y1=float(bbox[1]),
                                x2=float(bbox[2]),
                                y2=float(bbox[3]),
                            )
                            if bbox is not None
                            else None
                        ),
                    )
                )

            return RootInternalHealthResult(
                observation_id=observation_id,
                model_name=self.model.name,
                model_version=self.model.version,
                task=ModelTask(self.model.task),
                detections=detections,
                processing_time_ms=(
                    time.perf_counter() - started
                ) * 1000,
                evidence_quality=quality,
                status="COMPLETED",
            )

        except FileNotFoundError as exc:
            return self._error(
                observation_id,
                "IMAGE_NOT_FOUND",
                str(exc),
                started,
            )
        except Exception as exc:
            return self._error(
                observation_id,
                "INFERENCE_FAILED",
                str(exc),
                started,
            )

    def _error(self, observation_id, code, message, started):
        return RootInternalHealthResult(
            observation_id=observation_id,
            model_name=getattr(self.model, "name", "unknown"),
            model_version=getattr(self.model, "version", "unknown"),
            task=ModelTask(
                getattr(self.model, "task", "CLASSIFICATION")
            ),
            processing_time_ms=(
                time.perf_counter() - started
            ) * 1000,
            evidence_quality="UNKNOWN",
            status="FAILED",
            error_code=code,
            error_message=message,
        )
