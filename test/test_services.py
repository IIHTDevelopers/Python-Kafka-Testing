import unittest
from unittest.mock import patch, MagicMock
from kafka_app.services import TransactionManagementService
from kafka_app.transactions import Transaction
import os

class TestTransactionManagementService(unittest.TestCase):
    
    @patch('kafka_app.services.csv.DictReader')
    def test_load_transactions_from_csv(self, mock_csv):
        mock_csv.return_value = [
            {
                "account_from": "123",
                "account_to": "456",
                "amount": "1000",
                "location": "NY",
                "balance": "2000",
                "transaction_time": "2023-06-18T00:00:00",
                "account_age": "2",
                "transaction_frequency": "1"
            }
        ]
        
        tms = TransactionManagementService()
        tms.load_transactions_from_csv('test_data/test_transactions.csv')
        
        self.assertEqual(len(tms.get_all_transactions()), 1)
        transaction = tms.get_all_transactions()[0]
        self.assertEqual(transaction.account_from, "123")

if __name__ == '__main__':
    unittest.main()