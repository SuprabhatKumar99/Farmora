from app.kafka_integration.producer.producer import KafkaEventProducer


class DeadLetterPublisher:
    def __init__(self, producer=None, topic="ai.inference.dlq"):
        self.producer = producer or KafkaEventProducer()
        self.topic = topic

    def publish(self, event, key=None):
        self.producer.publish(self.topic, event, key=key)
