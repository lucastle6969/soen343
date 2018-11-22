from dpcontracts import invariant


@invariant("The number of borrowed items cannot exceed 10", lambda self: len(self.borrowed_items) <= 10)
class User:
    def __init__(self, user_id, first_name, last_name, address, email, phone, admin, password, borrowed_items=set(), cart=[]):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin
        self.password = password
        self.borrowed_items = borrowed_items
        self.cart = cart
