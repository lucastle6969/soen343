from model.Tdg import Tdg
from model.TransactionRegistry import TransactionRegistry
from dpcontracts import require, ensure

class TransactionMapper:

    def __init__(self, app, catalog):
        self.tdg = Tdg(app)
        self.transaction_registry = TransactionRegistry()
        self.transaction_registry.populate(self.tdg.get_transactions(), self.tdg.get_active_loans(), catalog)

    @ensure("All passed items must be marked as returned.",
            lambda args, result: all(args.self.transaction_registry.get_transaction(args.user_id, item, args.timestamp).transaction_type == 'return' for item in args.physical_items))
    def add_transactions(self, user_id, physical_items, transaction_type, timestamp):
        last_ids = self.tdg.add_transactions(user_id, physical_items, transaction_type, timestamp)
        self.transaction_registry.add_transactions(user_id, physical_items, transaction_type, timestamp, last_ids)
