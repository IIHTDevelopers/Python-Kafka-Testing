import json
import time
from kafka import KafkaProducer, KafkaConsumer

class TransactionProducer:
    def __init__(self, kafka_brokers, topic, retries=5):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
        self.retries = retries

    def send_message(self, message):
        for _ in range(self.retries):
            try:
                future = self.producer.send(self.topic, message)
                result = future.get(timeout=10)
                print(f"Message sent: {result}")
                return
            except Exception as e:
                print(f"Error sending message: {e}")
                time.sleep(1)
        print("Failed to send message after retries, sending to DLQ")
        self.send_to_dlq(message)

    def send_to_dlq(self, message):
        dlq_topic = f"{self.topic}_dlq"
        self.producer.send(dlq_topic, message)
