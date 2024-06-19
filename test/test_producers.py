import unittest
from unittest.mock import patch, MagicMock
from kafka_app.producers import TransactionProducer

class TestTransactionProducer(unittest.TestCase):

    @patch('kafka.KafkaProducer')
    def setUp(self, MockKafkaProducer):
        self.mock_kafka_producer = MockKafkaProducer.return_value
        self.producer = TransactionProducer(['localhost:9092'], 'transactions')
    
    def test_send_message_success(self):
        future = MagicMock()
        self.mock_kafka_producer.send.return_value = future
        future.get.return_value = "message sent"

        self.producer.send_message({"amount": 100})

        self.mock_kafka_producer.send.assert_called_once_with('transactions', {"amount": 100})

    def test_send_message_failure(self):
        future = MagicMock()
        self.mock_kafka_producer.send.side_effect = Exception("Kafka error")
        self.producer.send_to_dlq = MagicMock()

        self.producer.send_message({"amount": 100})

        self.producer.send_to_dlq.assert_called_once_with({"amount": 100})

if __name__ == '__main__':
    unittest.main()