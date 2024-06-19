import unittest
import json
from unittest.mock import MagicMock, patch
from kafka_app.consumers import TransactionConsumer

class TestTransactionConsumer(unittest.TestCase):

    @patch('kafka.KafkaProducer')
    @patch('kafka.KafkaConsumer')
    def setUp(self, MockKafkaConsumer, MockKafkaProducer):
        self.mock_kafka_consumer = MockKafkaConsumer.return_value
        self.mock_kafka_producer = MockKafkaProducer.return_value
        self.consumer = TransactionConsumer(['localhost:9092'], 'transactions')
    
    def test_is_suspicious(self):
        suspicious_transaction = {
            "amount": 200000,
            "location": "FL",
            "account_age": 0,
            "transaction_frequency": 100,
            "balance": -10,
            "description": "suspicious activity",
            "suspicious_keywords": ["suspicious", "fraud", "illegal"]
        }
        authentic_transaction = {
            "amount": 100,
            "location": "NY",
            "account_age": 2,
            "transaction_frequency": 10,
            "balance": 500,
            "description": "normal activity",
            "suspicious_keywords": ["suspicious", "fraud", "illegal"]
        }

        self.assertTrue(self.consumer.is_suspicious(suspicious_transaction))
        self.assertFalse(self.consumer.is_suspicious(authentic_transaction))
    
    @patch('kafka_app.consumers.TransactionConsumer.is_suspicious')
    def test_process_transactions(self, mock_is_suspicious):
        mock_is_suspicious.side_effect = [True, False]
        
        self.mock_kafka_consumer.__iter__.return_value = [
            MagicMock(value=json.dumps({"amount": 200000}).encode('utf-8')),
            MagicMock(value=json.dumps({"amount": 100}).encode('utf-8'))
        ]

        self.consumer.process_transactions()

        self.mock_kafka_producer.send.assert_any_call('suspicious', {"amount": 200000})
        self.mock_kafka_producer.send.assert_any_call('authentic', {"amount": 100})

if __name__ == '__main__':
    unittest.main()