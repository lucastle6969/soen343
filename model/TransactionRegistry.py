from model.Transaction import Transaction, ActiveLoan


class TransactionRegistry:

    def __init__(self):
        self.historical_registry = []
        self.active_loan_registry = []

    def add_transactions(self):
        pass

    def populate(self, all_transactions, active_loans):
        for entry in all_transactions:
            self.historical_registry.append(Transaction(entry[1], entry[2], entry[3], entry[4], entry[5]))
        for entry in active_loans:
            self.active_loan_registry.append(ActiveLoan(entry[1], entry[2], entry[3], entry[4]))
