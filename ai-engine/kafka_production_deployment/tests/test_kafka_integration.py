from app.kafka_integration.config.settings import KafkaSettings
from app.kafka_integration.retry.policy import RetryPolicy
from app.kafka_integration.schemas.events import InferenceRequestEvent
from app.kafka_integration.serialization.json_codec import (
    decode_event,
    encode_event,
)


def test_event_round_trip():
    event = InferenceRequestEvent(
        request_id="REQ-1",
        job_id="JOB-1",
        case_id="CASE-1",
        input_type="image",
        input_uri="object://input/image.jpg",
        model_version="production",
    )

    restored = decode_event(encode_event(event), InferenceRequestEvent)

    assert restored.request_id == "REQ-1"
    assert restored.input_type == "image"
    assert restored.model_version == "production"


def test_retry_policy():
    policy = RetryPolicy(max_retries=3)

    assert policy.should_retry(True, 0) is True
    assert policy.should_retry(True, 3) is False
    assert policy.should_retry(False, 0) is False


def test_topic_defaults():
    settings = KafkaSettings()

    assert settings.request_topic == "ai.inference.request"
    assert settings.completed_topic == "ai.inference.completed"
    assert settings.failed_topic == "ai.inference.failed"
    assert settings.dlq_topic == "ai.inference.dlq"
