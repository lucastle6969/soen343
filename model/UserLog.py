
class UserLog:
    def __init__(self, id, user_fk, log_type, timestamp):
        self.id = id
        self.user_fk = user_fk
        self.log_type = log_type
        self.timestamp = timestamp
