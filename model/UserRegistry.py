from model.User import User
from model.Item import PhysicalBook, PhysicalMagazine, PhysicalMovie, PhysicalMusic


class UserRegistry:

    def __init__(self):
        self.active_user_registry = []
        self.list_of_users = []
        self.catalog_lock = -1

    def populate(self, all_users):
        user_id = -1
        items = []
        for entry in all_users:
            if user_id != entry[0]:
                if user_id != -1:
                    current_user.borrowed_items = items[:]
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
        #to account for the last user
        current_user.borrowed_items = items[:]
        self.list_of_users.append(current_user)
            
    def check_lock(self):
        return self.catalog_lock

    def remove_lock(self):
        self.catalog_lock = -1

    def lock (self, user_id):
        self.catalog_lock = user_id

    def enlist_active_user(self, user_id, first_name, last_name, email, admin, timestamp, active_time, catalog_time, catalog_flag):
        self.active_user_registry.append((user_id, first_name, last_name, email, admin, timestamp, active_time, catalog_time, catalog_flag))

    def check_restart_session(self, session):
        online = False
        only_flashes = len(session) == 1 and '_flashes' in session
        for id, first_name, last_name, email, admin, time, active_time, catalog_time, catalog_flag in self.active_user_registry:
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

    def insert_user(self, user_id, first_name, last_name, address, email, phone, admin, password):
        self.list_of_users.append(User(user_id, first_name, last_name, address, email, phone, admin, password))

    def get_user_by_email(self, email):
        for user in self.list_of_users:
            if email == user.email:
                return user
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

    def remove_borrowed_items(self, user_id, prefix, item_fk, physical_id):
        for user in self.list_of_users:
            if user.id == user_id:
                for item in user.borrowed_items:
                    if item.prefix == prefix and item.item_fk == item_fk and item.id == physical_id:
                        user.borrowed_items.remove(item)
