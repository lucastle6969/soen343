from model.User import User


class UserRegistry:

    def __init__(self):
        self.active_user_registry = []
        self.list_of_users = []

    def populate(self, all_users):
        for entry in all_users:
            self.list_of_users.append(User(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7]))

    def enlist_active_user(self, data, timestamp):
        self.active_user_registry.append((data, timestamp))

    def check_restart_session(self, session):
        online = False
        only_flashes = len(session) == 1 and '_flashes' in session
        for id, time in self.active_user_registry:
            if 'user_id' in session and id == session['user_id']:
                online = True
        if not online and only_flashes:
            cleared = False
        elif not online and session:
            session.clear()
            cleared = True
        else:
            cleared = False
        return cleared

    def ensure_not_already_logged(self, user_id):
        # log user out if they are already logged in
        self.active_user_registry[:] = [tup for tup in self.active_user_registry if not user_id == tup[0]]

    def insert_user(self, user_id, firstname, lastname, address, email, phone, admin, password):
        self.list_of_users.append(User(user_id, firstname, lastname, address, email, phone, admin, password))

    def get_user_by_email(self, email):
        for user in self.list_of_users:
            if email == user.email:
                return user
            else:
                return None

    def validate_admin(self, user_id, admin):
        for tup in self.active_user_registry:
            if tup[0] == user_id and admin:
                return True
        return False

    def remove_from_active(self, user_id):
        self.active_user_registry[:] = [tup for tup in self.active_user_registry if not user_id == tup[0]]

    def get_active_users(self):
        return self.active_user_registry

    def get_all_users(self):
        return self.list_of_users
