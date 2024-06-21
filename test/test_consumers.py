import unittest
from unittest.mock import patch, MagicMock
from kafka_app.consumers import TransactionConsumer

class TestTransactionConsumer(unittest.TestCase):

    @patch('consumers.KafkaConsumer')
    @patch('consumers.KafkaProducer')
    def setUp(self, mock_producer, mock_consumer):
        self.consumer = TransactionConsumer(['localhost:9092'], 'test_topic')
    
    def test_is_suspicious(self):
        transaction = {
            "amount": 150000,
            "location": "NY",
            "account_age": 2,
            "transaction_frequency": 10,
            "balance": 500,
            "description": "test transaction"
        }
        self.assertTrue(self.consumer.is_suspicious(transaction))

    def test_process_transactions(self):
        self.consumer.is_suspicious = MagicMock(return_value=True)
        self.consumer.producer.send = MagicMock()
        self.consumer.consumer = MagicMock()
        self.consumer.consumer.__iter__.return_value = [
            MagicMock(value={
                "amount": 150000,
                "location": "NY",
                "account_age": 2,
                "transaction_frequency": 10,
                "balance": 500,
                "description": "test transaction"
            })
        ]
        self.consumer.process_transactions()
        self.consumer.producer.send.assert_called_with('suspicious', {
            "amount": 150000,
            "location": "NY",
            "account_age": 2,
            "transaction_frequency": 10,
            "balance": 500,
            "description": "test transaction"
        })

if __name__ == '__main__':
    unittest.main()