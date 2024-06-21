class Transaction:
    def __init__(self, account_from, account_to, amount, location, balance, transaction_time, account_age, transaction_frequency):
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount
        self.location = location
        self.balance = balance
        self.transaction_time = transaction_time
        self.account_age = account_age
        self.transaction_frequency = transaction_frequency