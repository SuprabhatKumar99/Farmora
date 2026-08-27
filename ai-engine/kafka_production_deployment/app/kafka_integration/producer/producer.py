from confluent_kafka import Producer

from app.kafka_integration.config.settings import KafkaSettings
from app.kafka_integration.serialization.json_codec import encode_event


class KafkaEventProducer:
    def __init__(self, settings: KafkaSettings | None = None):
        self.settings = settings or KafkaSettings()
        self.producer = Producer({
            "bootstrap.servers": self.settings.bootstrap_servers,
            "client.id": self.settings.client_id,
        })

    def publish(self, topic: str, event, key: str | None = None):
        self.producer.produce(
            topic=topic,
            key=key,
            value=encode_event(event),
        )
        self.producer.poll(0)
        self.producer.flush()
