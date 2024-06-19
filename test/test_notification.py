import unittest
from unittest.mock import patch, MagicMock
from kafka_app.notification import NotificationService

class TestNotificationService(unittest.TestCase):

    @patch('kafka_app.notification.smtplib.SMTP')
    @patch('kafka_app.notification.KafkaConsumer')
    def test_send_email(self, mock_kafka_consumer, mock_smtp):
        kafka_brokers = ['broker1', 'broker2']
        topics = ['suspicious']
        email_server = 'smtp.example.com'
        email_port = 587
        email_user = 'user@example.com'
        email_password = 'password'
        
        mock_kafka_consumer.return_value = MagicMock()
        
        notification_service = NotificationService(kafka_brokers, topics, email_server, email_port, email_user, email_password)
        
        notification_service.send_email('Subject', 'Body', 'to@example.com')
        
        instance = mock_smtp.return_value
        instance.sendmail.assert_called_with(
            'user@example.com', 
            ['to@example.com'], 
            'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Subject\nFrom: user@example.com\nTo: to@example.com\n\nBody'
        )

if __name__ == '__main__':
    unittest.main()