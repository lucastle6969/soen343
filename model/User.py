class User:
    def __init__(self, id, firstname, lastname, address, email, phone, admin, password):
        self.id = id
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
    def validate_admin(active_user_registry, id, admin):
        for tup in active_user_registry:
            if tup[0] == id and admin == True:
                return True
        return False

