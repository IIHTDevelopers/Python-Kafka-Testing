import unittest
import json
from unittest.mock import patch, MagicMock
from kafka_app.notification import NotificationService

class TestNotificationService(unittest.TestCase):

    @patch('kafka.KafkaConsumer')
    def setUp(self, MockKafkaConsumer):
        self.mock_kafka_consumer = MockKafkaConsumer.return_value
        self.notification_service = NotificationService(
            kafka_brokers=['localhost:9092'],
            topics=['suspicious'],
            email_server='smtp.example.com',
            email_port=587,
            email_user='user@example.com',
            email_password='password'
        )
    
    @patch('smtplib.SMTP')
    def test_send_email(self, MockSMTP):
        mock_smtp_instance = MockSMTP.return_value
        self.notification_service.send_email(
            subject='Test Subject',
            body='Test Body',
            to_email='recipient@example.com'
        )
        mock_smtp_instance.sendmail.assert_called_once_with(
            'user@example.com',
            ['recipient@example.com'],
            'Content-Type: text/plain; charset="us-ascii"\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n'
            'Subject: Test Subject\n'
            'From: user@example.com\n'
            'To: recipient@example.com\n'
            '\n'
            'Test Body'
        )

    @patch('kafka_app.notification.NotificationService.send_email')
    def test_run(self, mock_send_email):
        self.mock_kafka_consumer.__iter__.return_value = [
            MagicMock(topic='suspicious', value=json.dumps({"amount": 200000}).encode('utf-8'))
        ]

        self.notification_service.run()

        mock_send_email.assert_called_once_with(
            subject="Suspicious Transaction Alert",
            body='Suspicious transaction detected: {"amount": 200000}',
            to_email="user@example.com"
        )

if __name__ == '__main__':
    unittest.main()