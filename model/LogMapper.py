from model.Tdg import Tdg
from model.LogRegistry import LogRegistry


class LogMapper:

    def __init__(self, app):
        self.tdg = Tdg(app)
        self.log_registry = LogRegistry()
        self.log_registry.populate(self.tdg.get_logs())

    def add_log(self, user_id, log_type, timestamp):
        last_ids = self.tdg.add_log(user_id, log_type, timestamp)
        self.log_registry.add_log(user_id, log_type, timestamp)
