from confluent_kafka import Producer


def kafka_health(bootstrap_servers: str) -> dict:
    try:
        producer = Producer({"bootstrap.servers": bootstrap_servers})
        metadata = producer.list_topics(timeout=3)
        return {
            "status": "UP",
            "broker_count": len(metadata.brokers),
        }
    except Exception as exc:
        return {
            "status": "DOWN",
            "error": str(exc),
        }
