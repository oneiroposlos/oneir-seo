from datetime import datetime

from kafka import KafkaConsumer

from src.config import MOOD_KAFKA_TOPIC
import json


def consume_mood_embeddings_from_kafka(topic, bootstrap_servers='localhost:9093', group_id='mood-embeddings'):
    """
    Consume mood embedding data from a Kafka topic.

    :param topic: Kafka topic to consume the messages from
    :param bootstrap_servers: Kafka bootstrap servers, default is 'localhost:9092'
    :param group_id: Group ID for the consumer, default is 'mood-embeddings'
    """

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='latest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    print(f"Consuming from {topic} with group_id {group_id}")

    for message in consumer:
        print(datetime.today())
        print(message.value)
        # yield message.value


if __name__ == '__main__':
    consume_mood_embeddings_from_kafka(MOOD_KAFKA_TOPIC)
