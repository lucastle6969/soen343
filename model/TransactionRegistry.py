from model.Transaction import Transaction, ActiveLoan


class TransactionRegistry:

    def __init__(self):
        self.historical_registry = []
        self.active_loan_registry = []

    def add_transaction(self):
        pass