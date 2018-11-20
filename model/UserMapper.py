from flask import render_template, flash, redirect, url_for
from passlib.hash import sha256_crypt
from model.Form import RegisterForm
from model.UserRegistry import UserRegistry
from model.Tdg import UserTdg

CART_MAX_SIZE = 10
BORROWED_MAX_SIZE = 10


class UserMapper:
    def __init__(self, app):
        self.tdg = UserTdg(app)
        self.user_registry = UserRegistry()
        self.user_registry.populate(self.tdg.get_all_users_active_loans())

    def register(self, request_, tool):
        form = RegisterForm(request_.form)
        if request_.method == 'POST' and form.validate():
            if not (self.tdg.get_user_by_email(form.email.data)):
                if tool == 'create_admin':
                    is_admin = 1
                if tool == 'create_client':
                    is_admin = 0

                new_user_id = self.tdg.insert_user(form.first_name.data, form.last_name.data, form.address.data, form.email.data,
                                          form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))
                if new_user_id:
                    self.user_registry.insert_user(new_user_id, form.first_name.data, form.last_name.data, form.address.data, form.email.data,
                                          form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))
                if tool == 'create_admin':
                    flash('The new administrator has been registered', 'success')
                if tool == 'create_client':
                    flash('The new client has been registered', 'success')

                return redirect(url_for('admin_tools_default'))
            else:
                flash("This email has already been used.")
                return render_template('admin_tools.html', tool='create_admin', form=form)

        return render_template('admin_tools.html', tool=tool, form=form)

    def check_restart_session(self, session):
        return self.user_registry.check_restart_session(session)

    def get_user_by_email(self, email):
        return self.user_registry.get_user_by_email(email)

    def ensure_not_already_logged(self, user_id):
        self.user_registry.ensure_not_already_logged(user_id)

    def enlist_active_user(self, user_id, user_first_name, user_last_name, user_email, user_admin, timestamp, active_time, catalog_time, catalog_flag):
        self.user_registry.enlist_active_user(user_id, user_first_name, user_last_name, user_email, user_admin, timestamp, active_time, catalog_time, catalog_flag)

    def validate_admin(self, user_id, admin):
        return self.user_registry.validate_admin(user_id, admin)

    def get_active_users(self):
        return self.user_registry.get_active_users()

    def get_all_users(self):
        return self.user_registry.get_all_users()

    def remove_from_active(self, user_id):
        self.user_registry.remove_from_active(user_id)

    def validate_return(self):
        return self.user_registry.catalog_lock == -1

    def remove_borrowed_items(self, user_id, physical_items):
        for item in physical_items:
            self.user_registry.remove_borrowed_items(user_id, item.prefix, item.item_fk, item.id)

    def validate_cart_size(self, user_id):
        for user in self.user_registry.list_of_users:
            if user.id == user_id:
                return len(user.cart) < CART_MAX_SIZE

    def add_to_cart(self, user_id, available_copy):
        for user in self.user_registry.list_of_users:
            if user.id == user_id:
                user.cart.append(available_copy)

    def remove_from_cart(self, user_id, physical_item_prefix, physical_item_id):
        item_to_remove = None
        for user in self.user_registry.list_of_users:
            if user.id == user_id:
                for physical_item in user.cart:
                    if physical_item.prefix == physical_item_prefix and physical_item.id == physical_item_id:
                        item_to_remove = physical_item
                        break
                if item_to_remove is not None:
                    user.cart.remove(item_to_remove)
                    return "True"  # text used because comparison needs to work in javascript
                else:
                    return "False"

    def validate_loan(self, user_id, loan_size):
        valid_loan_state = [False, False]
        for user in self.user_registry.list_of_users:
            if user.id == user_id:
                valid_loan_state[0] = loan_size <= (BORROWED_MAX_SIZE - len(user.borrowed_items))
                break
        valid_loan_state[1] = self.user_registry.catalog_lock == -1
        return valid_loan_state

    def loan_items(self, user_id, loaned_items):
        items_to_remove_from_cart = []
        for user in self.user_registry.list_of_users:
            if user.id == user_id:
                for loaned_item in loaned_items:
                    user.borrowed_items.add(loaned_item)
                    for cart_item in user.cart:
                        if cart_item.prefix == loaned_item.prefix and cart_item.item_fk == loaned_item.item_fk and cart_item.id == loaned_item.id:
                            items_to_remove_from_cart.append(cart_item)
                for item in items_to_remove_from_cart:
                    user.cart.remove(item)

    def empty_cart(self, user_id):
        print("user_id param: ", user_id)
        for user in self.user_registry.list_of_users:
            print("user.id in loop: ", user.id)
            if user.id == user_id:
                user.cart = []
                return True
        return False

    def get_user_cart(self, user_id):
        if user_id is not None:
            for user in self.user_registry.list_of_users:
                if user.id == user_id:
                    return user.cart
        return None
