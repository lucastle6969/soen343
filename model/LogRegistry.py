from model.Log import Log


class LogRegistry:

    def __init__(self):
        self.historical_registry = []

    def add_log(self, user_id, log_type, timestamp):
        self.historical_registry.append(Log(user_id, log_type, timestamp))

    def populate(self, all_logs):
        for log_entry in all_logs:
            self.historical_registry.append(log_entry)