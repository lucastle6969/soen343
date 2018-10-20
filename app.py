from flask import Flask, render_template, flash, redirect, url_for, session, request
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper
from model.UserRegistry import UserRegistry
from passlib.hash import sha256_crypt
from model.Form import RegisterForm, BookForm, MagazineForm, MovieForm, MusicForm, Forms
import datetime
import time


app = Flask(__name__)
tdg = Tdg(app)
user_registry = UserRegistry()
user_registry.populate(tdg.get_all_users())
item_mapper = ItemMapper(app)


@app.before_request
def before_request():
    cleared = user_registry.check_restart_session(session)
    if cleared:
        flash('Automatically logged out due to a disconnect', 'warning')
        return redirect(url_for('home'))


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        user = user_registry.get_user_by_email(email)
        if user:
            # log user out if they are already logged in
            user_registry.ensure_not_already_logged(user.id)
            # add the user to the active user registry in the form of a tuple (user_id, timestamp)
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            user_registry.enlist_active_user(user.id, timestamp)

            # compare passwords
            if sha256_crypt.verify(password_candidate, user.password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['firstname'] = user.firstname
                session['user_id'] = user.id
                session['admin'] = user.admin

                flash('You are now logged in', 'success')
                return redirect(url_for('home'))

            else:
                error = 'Invalid login'
                app.logger.info('NOT MATCHED')
                return render_template('login.html', error=error, form=form)
        else:
            app.logger.info('NO USER')
            error = 'Email not found'
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)


def register(request_, tool):
    form = RegisterForm(request_.form)
    app.logger.info(tool)
    if request_.method == 'POST' and form.validate():
        if not (tdg.get_user_by_email(form.email.data)):
            if tool == 'create_admin':
                is_admin = 1
            if tool == 'create_client':
                is_admin = 0
                
            new_user_id = tdg.insert_user(form.firstname.data, form.lastname.data, form.address.data, form.email.data,
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


def add_book(request_):
    form = BookForm(request_.form)
    if request_.method == 'POST' and form.validate():
        item_mapper.add_book(form)
        flash('Book is ready to be added - save changes', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_book', form=form)


def add_magazine(request_):
    form = MagazineForm(request_.form)
    if request_.method == 'POST' and form.validate():
        catalog.add_item("Magazine", form)
        flash('Magazine was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_magazine', form=form)


def add_movie(request_):
    form = MovieForm(request_.form)
    if request_.method == 'POST' and form.validate():
        catalog.add_item("Movie", form)
        flash('Movie was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_movie', form=form)


def add_music(request_):
    form = MusicForm(request_.form)
    if request_.method == 'POST' and form.validate():
        catalog.add_item("Music", form)
        flash('Music was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_music', form=form)


@app.route('/admin_tools')
def admin_tools_default():
    if session['logged_in']:
        if user_registry.validate_admin(session['user_id'], session['admin']):
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('home'))


@app.route('/admin_tools/<tool>',  methods=['GET', 'POST'])
def admin_tools(tool):
    if session['logged_in']:
        if user_registry.validate_admin(session['user_id'], session['admin']):
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry=user_registry.get_active_users(), tool=tool)
            elif tool == 'create_admin' or tool == 'create_client':
                return register(request, tool)
            elif tool == 'catalog_manager':
                return render_template('admin_tools.html', tool=tool, catalog=item_mapper.get_catalog(), saved_changes=item_mapper.get_saved_changes())
            elif tool == 'view_users':
                list_of_users = user_registry.get_all_users()
                return render_template('admin_tools.html', tool=tool, list_of_users=list_of_users)
        else:
            flash('invalid tool')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('login'))


@app.route('/admin_tools/edit_entry/<item_id>', methods=['GET', 'POST'])
def edit_entry(item_id):
    # Obtain selected item from catalog
    item_selected = catalog.get_item_by_id(item_id)
    selected_item_type = item_selected.prefix

    # the Forms class has a getFormForItemType() which creates a form for the item type selected
    form = Forms.get_form_for_item_type(selected_item_type, request.form)

    if request.method == 'POST': 
        catalog.edit_item(item_id, form)
        return redirect('/admin_tools/catalog_manager')
    else:
        # Forms class has a getFormData() which returns a preloaded form with the data of the selected item
        form = Forms.get_form_data(item_selected, request)
        return render_template('admin_tools.html', form=form, prefix=selected_item_type, id=item_selected.id,
                               item="edit")


@app.route('/admin_tools/delete_entry/<id>',  methods=['POST'])
def delete_item(id):
    delete_success = catalog.delete_item(id)
    if delete_success:
        flash(f'Item (id {id}) deleted.', 'success')
        return redirect(url_for('admin_tools', tool='catalog_manager'))
    else:
        flash('Item not found.')
        return redirect(url_for('admin_tools', tool='catalog_manager'))


@app.route('/admin_tools/catalog_manager/<item>',  methods=['GET', 'POST'])
def catalog_manager(item):
    app.logger.info(item)
    if session['logged_in']:
        if user_registry.validate_admin(session['user_id'], session['admin']):
            app.logger.info(item)
            if item == 'add_movie':
                return add_movie(request)
            elif item == 'add_book':
                return add_book(request)
            elif item == 'add_magazine':
                return add_magazine(request)
            elif item == 'add_music':
                return add_music(request)
        else:
            flash('invalid item')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    user_registry.remove_from_active(session['user_id'])
    session.clear()

    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
