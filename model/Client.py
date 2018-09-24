

class Client:
    def __init__(self, data):
        self.id = data[0]
        self.firstname = data[1]
        self.lastname = data[2]
        self.address = data[3]
        self.email = data[4]
        self.phone = data[5]
        self.admin = data[6]
        self.password = data[7]

    # Getters and setters (not necessary for now)