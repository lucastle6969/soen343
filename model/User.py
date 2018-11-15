
class User:
    def __init__(self, user_id, first_name, last_name, address, email, phone, admin, password, borrowed_items = [], cart = []):
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
