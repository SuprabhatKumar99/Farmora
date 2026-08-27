import time

from app.experts.expert7_treatment_management.inference.inference_engine import (
    TreatmentManagementInferenceEngine,
)
from app.experts.expert7_treatment_management.inference.prediction_adapter import (
    TreatmentPredictionAdapter,
)
from app.experts.expert7_treatment_management.preprocessing.input import (
    TreatmentManagementPreprocessor,
)
from app.experts.expert7_treatment_management.postprocessing.postprocessor import (
    TreatmentManagementPostprocessor,
)
from app.experts.expert7_treatment_management.schemas.models import (
    ModelTask,
    TreatmentCandidate,
    TreatmentManagementResult,
)


class Expert7TreatmentManagementService:
    """Expert 7 orchestration for treatment/management evidence."""

    def __init__(
        self,
        model=None,
        preprocessor=None,
        inference_engine=None,
        adapter=None,
        postprocessor=None,
    ):
        self.model = model
        self.preprocessor = preprocessor or TreatmentManagementPreprocessor()
        self.inference_engine = inference_engine
        self.adapter = adapter or TreatmentPredictionAdapter()
        self.postprocessor = (
            postprocessor or TreatmentManagementPostprocessor()
        )

    def set_model(self, model):
        self.model = model
        self.inference_engine = TreatmentManagementInferenceEngine(model)

    def analyze(self, case_id: str, input_path: str) -> TreatmentManagementResult:
        started = time.perf_counter()

        if self.model is None:
            return self._error(
                case_id,
                "MODEL_NOT_LOADED",
                "Expert 7 model is not loaded.",
                started,
            )

        try:
            dataframe = self.preprocessor.load(input_path)

            engine = self.inference_engine or TreatmentManagementInferenceEngine(
                self.model
            )

            raw = engine.run(dataframe)
            candidates = self.adapter.adapt(raw)
            candidates = self.postprocessor.process(candidates)

            treatments = [
                TreatmentCandidate(**item)
                for item in candidates
            ]

            return TreatmentManagementResult(
                case_id=case_id,
                model_name=self.model.name,
                model_version=self.model.version,
                task=ModelTask(self.model.task),
                treatments=treatments,
                processing_time_ms=(
                    time.perf_counter() - started
                ) * 1000,
                evidence_quality="ACCEPTABLE",
                status="COMPLETED",
            )

        except FileNotFoundError as exc:
            return self._error(
                case_id,
                "INPUT_NOT_FOUND",
                str(exc),
                started,
            )
        except Exception as exc:
            return self._error(
                case_id,
                "INFERENCE_FAILED",
                str(exc),
                started,
            )

    def _error(self, case_id, code, message, started):
        return TreatmentManagementResult(
            case_id=case_id,
            model_name=getattr(self.model, "name", "unknown"),
            model_version=getattr(self.model, "version", "unknown"),
            task=ModelTask(
                getattr(self.model, "task", "RECOMMENDATION")
            ),
            processing_time_ms=(
                time.perf_counter() - started
            ) * 1000,
            evidence_quality="UNKNOWN",
            status="FAILED",
            error_code=code,
            error_message=message,
        )
