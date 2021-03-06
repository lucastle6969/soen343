from model.User import User
from model.UserLog import UserLog
from model.Item import PhysicalBook, PhysicalMagazine, PhysicalMovie, PhysicalMusic


class UserRegistry:

    def __init__(self):
        self.list_of_users = []
        self.active_user_registry = []
        self.historical_user_log_registry = []
        self.catalog_lock = -1

    def populate(self, all_users):
        user_id = -1
        items = []
        for entry in all_users:
            if user_id != entry[0]:
                if user_id != -1:
                    current_user.borrowed_items = set(items[:])
                    self.list_of_users.append(current_user)
                user_id = entry[0]
                current_user = User(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7])
                items = []
            if entry[8] is not None:
                    # (id, fk, status, return_date, user_fk)
                    items.append(PhysicalBook(entry[8], entry[9], entry[10], entry[11], entry[12]))
            if entry[13] is not None:
                    items.append(PhysicalMusic(entry[13], entry[14], entry[15], entry[16], entry[17]))
            if entry[18] is not None:
                    items.append(PhysicalMovie(entry[18], entry[19], entry[20], entry[21], entry[22]))
        # to account for the last user
        current_user.borrowed_items = set(items[:])
        self.list_of_users.append(current_user)

    def populate_historical_log(self, all_logs):
        self.historical_user_log_registry = []
        for log_entry in all_logs:
            self.historical_user_log_registry.append(UserLog(log_entry[0], log_entry[1], log_entry[2], log_entry[3]))

    def add_log(self, user_id, log_type, timestamp, historical_log_id):
        self.historical_user_log_registry.append(UserLog(historical_log_id, user_id, log_type, timestamp))

    def check_lock(self):
        return self.catalog_lock

    def remove_lock(self):
        self.catalog_lock = -1

    def lock(self, user_id):
        self.catalog_lock = user_id

    def enlist_active_user(self, user_id, first_name, last_name, email, admin, timestamp, active_time, catalog_time, catalog_flag):
        self.active_user_registry.append((user_id, first_name, last_name, email, admin, timestamp, active_time, catalog_time, catalog_flag))

    def check_restart_session(self, session):
        online = False
        cleared = False
        reason = None
        user_id = None
        only_flashes = len(session) == 1 and '_flashes' in session
        for id, first_name, last_name, email, admin, time, active_time, catalog_time, catalog_flag in self.active_user_registry:
            if 'user_id' in session and id == session['user_id']:
                online = True
                if session['timestamp'] != time:
                    user_id = session['user_id']
                    session.clear()
                    reason = 'simultaneous'
                    cleared = True
        if not online and only_flashes:
            cleared = False
        elif not online and session:
            if 'user_id' in session:
                user_id = session['user_id']
            session.clear()
            cleared = True
            reason = 'disconnect'
        elif not cleared:
            cleared = False
        result = [cleared, reason, user_id]
        return result

    def ensure_not_already_logged(self, user_id):
        # log user out if they are already logged in
        active_size_before = len(self.active_user_registry)
        self.active_user_registry[:] = [tup for tup in self.active_user_registry if not user_id == tup[0]]
        if len(self.active_user_registry) < active_size_before:
            return False
        else:
            return True

    def insert_user(self, user_id, first_name, last_name, address, email, phone, admin, password):
        self.list_of_users.append(User(user_id, first_name, last_name, address, email, phone, admin, password))

    def get_user_by_email(self, email):
        for user in self.list_of_users:
            if email == user.email:
                return user
        return None

    def get_user_by_id(self, user_id):
        for user in self.list_of_users:
            if user_id == user.id:
                return user
        return None

    def validate_admin(self, user_id, admin):
        for tup in self.active_user_registry:
            if tup[0] == user_id and admin:
                return True
        return False

    def remove_user_from_list(self, user_id):
        for user in self.list_of_users:
            if int(user_id) == user.id:
                self.list_of_users.remove(user)

    def remove_from_active(self, user_id):
        self.active_user_registry[:] = [tup for tup in self.active_user_registry if not user_id == tup[0]]

    def get_active_users(self):
        return self.active_user_registry

    def get_all_users(self):
        self.list_of_users.sort(key=self.sort_list_of_users)
        return self.list_of_users

    def get_borrowed_items(self, user_id, prefix, item_fk, physical_id):
        for user in self.list_of_users:
            if user.id == user_id:
                to_return = []
                for item in user.borrowed_items:
                    if item.prefix == prefix and item.item_fk == item_fk and item.id == physical_id:
                        to_return.append(item)

                return to_return

    def sort_list_of_users(self, user):
        return user.id

    def empty_list_of_users(self):
        self.list_of_users = []

    def remove_borrowed_items(self, user_id, prefix, item_fk, physical_id):
        for user in self.list_of_users:
            if user.id == user_id:
                to_remove = []
                for item in user.borrowed_items:
                    if item.prefix == prefix and item.item_fk == item_fk and item.id == physical_id:
                        to_remove.append(item)
                for item_re in to_remove:
                    user.borrowed_items.remove(item_re)

    def get_physical_item(self, user_id, prefix, item_fk, physical_id):
        for user in self.list_of_users:
            if user.id == user_id:
                for item in user.borrowed_items:
                    if item.prefix == prefix and item.item_fk == item_fk and item.id == physical_id:
                        return item
        return None
