
class Transaction:
    def __init__(self, transaction_id, user_fk, physical_item):
        self.transaction_id = transaction_id
        self.user_fk = user_fk
        self.physical_item = physical_item


class HistoricalTransaction(Transaction):
    def __init__(self, transaction_id, user_fk, physical_item, transaction_type, timestamp):
        Transaction.__init__(self, transaction_id, user_fk, physical_item)
        self.transaction_type = transaction_type
        self.timestamp = timestamp


class ActiveLoan(Transaction):
    def __init__(self, transaction_id, user_fk, physical_item, return_date):
        Transaction.__init__(self, transaction_id, user_fk, physical_item)
        self.return_date = return_date
