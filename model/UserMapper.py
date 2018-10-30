from flask import render_template, flash, redirect, url_for
from passlib.hash import sha256_crypt
from model.Form import RegisterForm


class UserMapper:
    def __init__(self, tdg):
        self.tdg = tdg

    def register(self, request_, tool, user_registry):
        form = RegisterForm(request_.form)
        if request_.method == 'POST' and form.validate():
            if not (self.tdg.get_user_by_email(form.email.data)):
                if tool == 'create_admin':
                    is_admin = 1
                if tool == 'create_client':
                    is_admin = 0

                new_user_id = self.tdg.insert_user(form.firstname.data, form.lastname.data, form.address.data, form.email.data,
                                          form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))
                if new_user_id:
                    user_registry.insert_user(new_user_id, form.firstname.data, form.lastname.data, form.address.data, form.email.data,
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
