from model.Transaction import HistoricalTransaction, ActiveLoan


class TransactionRegistry:

    def __init__(self):
        self.historical_registry = []
        self.active_loan_registry = []

    def add_transactions(self, user_id, physical_items, transaction_type, timestamp, next_ids):
        transaction_id = next_ids.historical
        for item in physical_items:
            self.historical_registry.append(HistoricalTransaction(transaction_id, user_id, item, transaction_type, timestamp))
            transaction_id = transaction_id + 1
            if transaction_type is "loan":
                active_loan_id = next_ids.active
                self.active_loan_registry.append(ActiveLoan(active_loan_id, user_id, item, item.return_date))
                active_loan_id = active_loan_id + 1
            elif transaction_type is "return":
                for active_loan in self.active_loan_registry:
                    if active_loan.user_fk is user_id and active_loan.physical_item.prefix is item.prefix and active_loan.physical_item.id is item.id:
                        self.active_loan_registry.remove(item)

    def populate(self, all_transactions, active_loans):
        for entry in all_transactions:
            self.historical_registry.append(HistoricalTransaction(entry[1], entry[2], entry[3], entry[4], entry[5]))
        for entry in active_loans:
            self.active_loan_registry.append(ActiveLoan(entry[1], entry[2], entry[3], entry[4]))
