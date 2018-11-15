from flask import render_template, flash, redirect, url_for
from passlib.hash import sha256_crypt
from model.Form import RegisterForm
from model.UserRegistry import UserRegistry
from model.Tdg import Tdg


class UserMapper:
    def __init__(self, app):
        self.tdg = Tdg(app)
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
