from confluent_kafka import Consumer, KafkaException

from app.kafka_integration.config.settings import KafkaSettings
from app.kafka_integration.schemas.events import InferenceRequestEvent
from app.kafka_integration.serialization.json_codec import decode_event


class KafkaInferenceConsumer:
    def __init__(self, handler, settings=None):
        self.settings = settings or KafkaSettings()
        self.handler = handler
        self.consumer = Consumer({
            "bootstrap.servers": self.settings.bootstrap_servers,
            "group.id": self.settings.group_id,
            "client.id": self.settings.client_id + "-consumer",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        })

    def run(self):
        self.consumer.subscribe([self.settings.request_topic])

        try:
            while True:
                message = self.consumer.poll(1.0)

                if message is None:
                    continue

                if message.error():
                    raise KafkaException(message.error())

                event = decode_event(
                    message.value(),
                    InferenceRequestEvent,
                )

                self.handler(event)
                self.consumer.commit(message=message, asynchronous=False)
        finally:
            self.consumer.close()
