from model.Tdg import TransactionTdg
from model.TransactionRegistry import TransactionRegistry


class TransactionMapper:

    def __init__(self, app, catalog):
        self.tdg = TransactionTdg(app)
        self.transaction_registry = TransactionRegistry()
        self.transaction_registry.populate(self.tdg.get_transactions(), self.tdg.get_active_loans(), catalog)

    def add_transactions(self, user_id, physical_items, transaction_type, timestamp):
        last_ids = self.tdg.add_transactions(user_id, physical_items, transaction_type, timestamp)
        self.transaction_registry.add_transactions(user_id, physical_items, transaction_type, timestamp, last_ids)
