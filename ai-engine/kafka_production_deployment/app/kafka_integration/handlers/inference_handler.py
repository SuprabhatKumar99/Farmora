from app.kafka_integration.schemas.events import (
    InferenceCompletedEvent,
    InferenceFailedEvent,
)


class InferenceEventHandler:
    """Adapter between Kafka events and the existing AI inference service.

    The callable `inference_service` must be supplied by the existing
    production AI engine. No fake inference is performed here.
    """

    def __init__(self, inference_service):
        self.inference_service = inference_service

    def handle(self, event):
        try:
            result = self.inference_service.process_event(event)

            return InferenceCompletedEvent(
                request_id=event.request_id,
                job_id=event.job_id,
                case_id=event.case_id,
                status="COMPLETED",
                result=result,
                model_version=event.model_version,
            )
        except Exception as exc:
            return InferenceFailedEvent(
                request_id=event.request_id,
                job_id=event.job_id,
                case_id=event.case_id,
                error_code="INFERENCE_FAILED",
                error_message=str(exc),
                model_version=event.model_version,
                retryable=False,
            )
