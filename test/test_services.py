import unittest
from kafka_app.services import TransactionManagementService
from kafka_app.transactions import Transaction
import os

class TestTransactionManagementService(unittest.TestCase):

    def setUp(self):
        self.service = TransactionManagementService()
        self.test_csv_file = 'test_data/test_transactions.csv'

    def test_add_transaction(self):
        transaction = Transaction(
            account_from="123",
            account_to="456",
            amount=100.0,
            location="NY",
            balance=500.0,
            transaction_time="2024-06-14T12:00:00",
            account_age=2,
            transaction_frequency=10
        )
        self.service.add_transaction(transaction)
        self.assertEqual(len(self.service.transactions), 1)
        self.assertEqual(self.service.transactions[0].account_from, "123")
    
    def test_load_transactions_from_csv(self):
        self.service.load_transactions_from_csv(self.test_csv_file)
        self.assertEqual(len(self.service.transactions), 3)
        self.assertEqual(self.service.transactions[0].account_from, "111")

    def test_get_all_transactions(self):
        transaction = Transaction(
            account_from="123",
            account_to="456",
            amount=100.0,
            location="NY",
            balance=500.0,
            transaction_time="2024-06-14T12:00:00",
            account_age=2,
            transaction_frequency=10
        )
        self.service.add_transaction(transaction)
        transactions = self.service.get_all_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].account_from, "123")

if __name__ == '__main__':
    unittest.main()