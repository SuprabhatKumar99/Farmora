import os


class KafkaSettings:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    client_id = os.getenv("KAFKA_CLIENT_ID", "agri-ai-engine")
    group_id = os.getenv("KAFKA_CONSUMER_GROUP", "agri-ai-engine")
    request_topic = os.getenv(
        "KAFKA_INFERENCE_REQUEST_TOPIC",
        "ai.inference.request",
    )
    completed_topic = os.getenv(
        "KAFKA_INFERENCE_COMPLETED_TOPIC",
        "ai.inference.completed",
    )
    failed_topic = os.getenv(
        "KAFKA_INFERENCE_FAILED_TOPIC",
        "ai.inference.failed",
    )
    followup_topic = os.getenv(
        "KAFKA_FOLLOWUP_TOPIC",
        "followup.feedback.received",
    )
    dlq_topic = os.getenv(
        "KAFKA_DLQ_TOPIC",
        "ai.inference.dlq",
    )
