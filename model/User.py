active_user_registry = []


class User:
    def __init__(self, user_id, firstname, lastname, address, email, phone, admin, password):
        self.id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin
        self.password = password


class Client(User):
    pass


class Admin(User):
    @staticmethod
    def validate_admin(user_registry, user_id, admin):
        for tup in user_registry:
            if tup[0] == user_id and admin:
                return True
        return False
