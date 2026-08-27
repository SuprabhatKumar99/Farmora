import time

from app.experts.expert6_prevention_ipm.preprocessing.input import (
    PreventionIPMPreprocessor,
)
from app.experts.expert6_prevention_ipm.schemas.models import (
    PreventionAction,
    PreventionIPMResult,
    ModelTask,
)


class Expert6PreventionIPMService:
    """Expert 6 orchestration.

    Produces structured prevention/IPM evidence or model-derived action
    candidates. It does not independently override verified agricultural
    knowledge or make the final decision.
    """

    def __init__(self, model=None, preprocessor=None):
        self.model = model
        self.preprocessor = preprocessor or PreventionIPMPreprocessor()

    def set_model(self, model):
        self.model = model

    def analyze(self, case_id: str, input_path: str) -> PreventionIPMResult:
        started = time.perf_counter()

        if self.model is None:
            return self._error(
                case_id,
                "MODEL_NOT_LOADED",
                "Expert 6 model is not loaded.",
                started,
            )

        try:
            dataframe = self.preprocessor.load(input_path)
            raw = self.model.predict(dataframe)

            actions = []
            for item in raw or []:
                actions.append(
                    PreventionAction(
                        action_id=str(item["action_id"]),
                        action_type=str(item["action_type"]),
                        priority=float(item["priority"]),
                        evidence_ids=[
                            str(x) for x in item.get("evidence_ids", [])
                        ],
                    )
                )

            return PreventionIPMResult(
                case_id=case_id,
                model_name=self.model.name,
                model_version=self.model.version,
                task=ModelTask(self.model.task),
                actions=actions,
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
        return PreventionIPMResult(
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
