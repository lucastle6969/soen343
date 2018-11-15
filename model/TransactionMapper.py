from model.Item import PhysicalBook, PhysicalMovie, PhysicalMusic
from model.Uow import Uow
from model.User import User
from model.Tdg import Tdg
from model.TransactionRegistry import TransactionRegistry


class TransactionMapper:

    def __init__(self, app):
        self.tdg = Tdg(app)
        self.transaction_registry = TransactionRegistry()
        self.transaction_registry.populate(self.tdg.get_transactions(), self.tdg.get_active_loans())

    def add_transactions(self, user_id, physical_items, transaction_type, timestamp):
        self.transaction_registry.add_transactions(user_id, physical_items, transaction_type, timestamp)
        self.tdg.add_transactions(user_id, physical_items, transaction_type, timestamp)

