import unittest
from unittest.mock import patch, MagicMock
from kafka_app.producers import TransactionProducer

class TestTransactionProducer(unittest.TestCase):

    @patch('producers.KafkaProducer')
    def setUp(self, mock_producer):
        self.producer = TransactionProducer(['localhost:9092'], 'test_topic')

    def test_send_message(self):
        self.producer.producer.send = MagicMock()
        self.producer.send_message({"key": "value"})
        self.producer.producer.send.assert_called_with('test_topic', {"key": "value"})

if __name__ == '__main__':
    unittest.main()