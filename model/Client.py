

class Client:
    def __init__(self, id, firstname, lastname, address, email, phone, admin, password):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin
        self.password = password

    # Getters and setters (not necessary for now)