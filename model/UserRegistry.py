from model.User import User, Admin, Client

class UserRegistry:
    
    def __init__(self):
        self.active_user_registry = []
        self.list_of_users = []
    
    def enlist_active_user(self, data, timestamp):
        self.active_user_registry.append((data, timestamp))

    