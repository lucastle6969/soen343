from model.Transaction import Transaction
class TransactionRegistry:

    def __init__(self):
        self.historical_registry = Transaction()
        self.active_loan_registry = ActiveLoan()

    def add_transaction(self):