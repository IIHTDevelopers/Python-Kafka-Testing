import json
import smtplib
from email.mime.text import MIMEText
from kafka import KafkaProducer, KafkaConsumer

class NotificationService:
    def __init__(self, kafka_brokers, topics, email_server, email_port, email_user, email_password):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=kafka_brokers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        self.email_server = email_server
        self.email_port = email_port
        self.email_user = email_user
        self.email_password = email_password

    def send_email(self, subject, body, to_email):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = to_email

        with smtplib.SMTP(self.email_server, self.email_port) as server:
            server.login(self.email_user, self.email_password)
            server.sendmail(self.email_user, [to_email], msg.as_string())

    def run(self):
        for message in self.consumer:
            if message.topic == 'suspicious':
                subject = "Suspicious Transaction Alert"
                body = f"Suspicious transaction detected: {message.value}"
                self.send_email(subject, body, "user@example.com")
