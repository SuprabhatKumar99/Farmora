import time

from app.expert8_core_ai.preprocessing.context import DecisionContextPreprocessor
from app.expert8_core_ai.prompting.builder import DecisionPromptBuilder
from app.expert8_core_ai.inference.inference_engine import DecisionInferenceEngine
from app.expert8_core_ai.inference.output_parser import DecisionOutputParser
from app.expert8_core_ai.postprocessing.decision_validator import DecisionValidator
from app.expert8_core_ai.validation.evidence_guard import EvidenceGuard
from app.expert8_core_ai.schemas.models import DecisionResult, DecisionStatus


class Expert8DecisionService:
    """Orchestrate Expert 8 from fused evidence to structured decision."""

    def __init__(self, model=None):
        self.model = model
        self.preprocessor = DecisionContextPreprocessor()
        self.prompt_builder = DecisionPromptBuilder()
        self.parser = DecisionOutputParser()
        self.validator = DecisionValidator()
        self.guard = EvidenceGuard()
        self.inference_engine = (
            DecisionInferenceEngine(model) if model else None
        )

    def set_model(self, model):
        self.model = model
        self.inference_engine = DecisionInferenceEngine(model)

    def decide(self, case_id: str, evidence_context: dict) -> DecisionResult:
        started = time.perf_counter()

        if self.model is None:
            return self._error(
                case_id,
                "MODEL_NOT_LOADED",
                "Expert 8 model is not loaded.",
                started,
            )

        try:
            context = self.preprocessor.prepare(evidence_context)
            self.guard.check(context)
            prompt = self.prompt_builder.build(context)
            raw = self.inference_engine.run(prompt)
            parsed = self.parser.parse(raw)
            decision = self.validator.validate(parsed)

            status = (
                DecisionStatus.VALIDATION_REQUIRED
                if decision.expert_or_lab_validation_required
                else DecisionStatus.COMPLETED
            )

            return DecisionResult(
                case_id=case_id,
                model_name=self.model.name,
                model_version=self.model.version,
                status=status,
                decision=decision,
                processing_time_ms=(
                    time.perf_counter() - started
                ) * 1000,
            )

        except ValueError as exc:
            return self._error(
                case_id,
                "INVALID_MODEL_OUTPUT_OR_CONTEXT",
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
        return DecisionResult(
            case_id=case_id,
            model_name=getattr(self.model, "name", "unknown"),
            model_version=getattr(self.model, "version", "unknown"),
            status=DecisionStatus.FAILED,
            processing_time_ms=(
                time.perf_counter() - started
            ) * 1000,
            error_code=code,
            error_message=message,
        )
