import json
from kafka import KafkaProducer, KafkaConsumer

class TransactionConsumer:
    def __init__(self, kafka_brokers, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_brokers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        self.authentic_topic = "authentic"
        self.suspicious_topic = "suspicious"
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def process_transactions(self):
        for message in self.consumer:
            transaction = message.value
            if self.is_suspicious(transaction):
                self.producer.send(self.suspicious_topic, transaction)
            else:
                self.producer.send(self.authentic_topic, transaction)

    def is_suspicious(self, transaction):
        if transaction["amount"] > 100000:
            return True
        if transaction["location"] not in ["NY", "CA", "TX"]:
            return True
        if transaction["account_age"] < 1:
            return True
        if transaction["transaction_frequency"] > 50:
            return True
        if transaction["balance"] < 0:
            return True
        if "suspicious_keywords" in transaction and any(keyword in transaction["description"] for keyword in transaction["suspicious_keywords"]):
            return True
        return False
