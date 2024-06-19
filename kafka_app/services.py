import csv
from .transactions import Transaction

class TransactionManagementService:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def load_transactions_from_csv(self, csv_file):
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                transaction = Transaction(
                    account_from=row["account_from"],
                    account_to=row["account_to"],
                    amount=float(row["amount"]),
                    location=row["location"],
                    balance=float(row["balance"]),
                    transaction_time=row["transaction_time"],
                    account_age=int(row["account_age"]),
                    transaction_frequency=int(row["transaction_frequency"])
                )
                self.add_transaction(transaction)

    def get_all_transactions(self):
        return self.transactions