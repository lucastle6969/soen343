from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from model.ItemMapper import ItemMapper
from model.UserMapper import UserMapper
from model.TransactionMapper import TransactionMapper
from passlib.hash import sha256_crypt
from model.Form import RegisterForm, BookForm, MagazineForm, MovieForm, MusicForm, SearchForm, Forms, OrderForm
from apscheduler.schedulers.background import BackgroundScheduler
from time import localtime, strftime

import datetime
import time


app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
item_mapper = ItemMapper(app)
user_mapper = UserMapper(app)
transaction_mapper = TransactionMapper(app, item_mapper.catalog.item_catalog)

ACTIVE_USER_GRACE_PERIOD = 2400
CATALOG_MANAGER_GRACE_PERIOD = 600
SECONDS_CLEAN_ACTIVE_USERS = 300
SECONDS_CLEAN_CATALOG_USERS = 120


def active_users():
    for user in user_mapper.user_registry.active_user_registry:
        if time.time() - user[6] > ACTIVE_USER_GRACE_PERIOD:
            user_to_remove = user[0]
            user_mapper.remove_from_active(user_to_remove)
            locker = user_mapper.user_registry.check_lock()
            if locker == user[0]:
                user_mapper.user_registry.remove_lock()


def catalog_users():
    for user in user_mapper.user_registry.active_user_registry:
        if time.time() - user[7] > CATALOG_MANAGER_GRACE_PERIOD and user[8]:
            user_as_list = list(user)
            user_as_list[7] = 0
            user_mapper.remove_from_active(user[0])
            user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
            locker = user_mapper.user_registry.check_lock()
            if locker == user[0]:
                user_mapper.user_registry.remove_lock()


sched = BackgroundScheduler(daemon=True)
sched.add_job(active_users, 'interval', seconds=SECONDS_CLEAN_ACTIVE_USERS)
sched.add_job(catalog_users, 'interval', seconds=SECONDS_CLEAN_CATALOG_USERS)
sched.start()


@app.before_request
def before_request():
    if len(session) > 0 and not (len(session) == 1 and '_flashes' in session):
        user_id = session['user_id']
        for user in user_mapper.user_registry.active_user_registry:
            if user[0] == user_id:
                user_as_list = list(user)
                user_as_list[6] = time.time()
                user_mapper.remove_from_active(session['user_id'])
                user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
                if "catalog_manager" in request.path and user[8]:
                    if time.time() - user[7] > CATALOG_MANAGER_GRACE_PERIOD:
                        user_as_list = list(user)
                        user_as_list[8] = False
                        user_mapper.remove_from_active(session['user_id'])
                        user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
                        item_mapper.uow = None
                        locker = user_mapper.user_registry.check_lock()
                        if locker == session['user_id']:
                            user_mapper.user_registry.remove_lock()
                        flash('You have been removed from the catalog manager for inactivity, changes were not saved.', 'warning')
                        return redirect(url_for('home'))
                    else:
                        user_as_list = list(user)
                        user_as_list[7] = time.time()
                        user_mapper.remove_from_active(session['user_id'])
                        user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
    result = user_mapper.check_restart_session(session)
    if result[0]:
        if result[1] == 'simultaneous':
            flash('Your account has been logged in from another location, you have been automatically logged out.', 'warning')
        if result[1] == 'disconnect':
            flash('Automatically logged out due to a disconnect/inactivity.', 'warning')
        return redirect(url_for('home'))


@app.route('/')
def index():
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        user_id = None
    # Default table view shows all books
    return render_template('home.html', item_list=item_mapper.get_all_items("bb", user_mapper.get_user_cart(user_id)), item="bb")


@app.route('/home')
def home():
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        user_id = None
    # Default table view shows all books
    return render_template('home.html', item_list=item_mapper.get_all_items("bb", user_mapper.get_user_cart(user_id)), item="bb")


@app.route('/home/<item>')
def itemList(item):
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        user_id = None
    if item == "bb":
        return render_template('home.html', item_list=item_mapper.get_all_items("bb", user_mapper.get_user_cart(user_id)), item="bb")
    elif item == "ma":
        return render_template('home.html', item_list=item_mapper.get_all_items("ma", user_mapper.get_user_cart(user_id)), item="ma")
    elif item == "mu":
        return render_template('home.html', item_list=item_mapper.get_all_items("mu", user_mapper.get_user_cart(user_id)), item="mu")
    elif item == "mo":
        return render_template('home.html', item_list=item_mapper.get_all_items("mo", user_mapper.get_user_cart(user_id)), item="mo")


@app.route('/home/search/<item>', methods=['GET', 'POST'])
def search(item):
    form = SearchForm(request.form)
    if item == 'books':
        return render_template('home.html', item_list=item_mapper.get_filtered_items("bb", form), item="bb")
    elif item == 'magazines':
        return render_template('home.html', item_list=item_mapper.get_filtered_items("ma", form), item="ma")
    elif item == 'movies':
        return render_template('home.html', item_list=item_mapper.get_filtered_items("mo", form), item="mo")
    elif item == 'music':
        return render_template('home.html', item_list=item_mapper.get_filtered_items("mu", form), item="mu")


@app.route('/home/order/<item_prefix>', methods=['GET', 'POST'])
def order(item_prefix):
    form = OrderForm(request.form)
    return render_template('home.html', item_list=item_mapper.get_ordered_items(form), item=item_prefix)


@app.route('/home/add_to_cart/<item_prefix>/<item_id>')
def add_to_cart(item_prefix, item_id):
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        return redirect('/home')
    valid_cart_size = user_mapper.validate_cart_size(user_id)
    if valid_cart_size:
        available_copy = item_mapper.get_available_copy(item_prefix, int(item_id), user_mapper.get_user_cart(user_id))
        if available_copy is not None:
            user_mapper.add_to_cart(user_id, available_copy)
            response = "added"
        else:
            response = "unavailable"
    else:
        response = "full"
    return jsonify(result=response, item_prefix=item_prefix, item_id=item_id)


@app.route('/cart/remove_from_cart/<physical_item_prefix>/<physical_item_id>')
def remove_from_cart(physical_item_prefix, physical_item_id):
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        return redirect('/home')
    response = user_mapper.remove_from_cart(user_id, physical_item_prefix, int(physical_item_id))
    return jsonify(result=response, physical_item_prefix=physical_item_prefix, physical_item_id=physical_item_id)


@app.route('/cart/empty_cart')
def empty_cart():
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        return redirect('/home')
    if user_mapper.empty_cart(user_id):
        flash('Items were successfully removed from your cart.', 'success')
        return redirect('/home')
    else:
        flash('Items were not successfully removed from cart. please, try again later.', 'warning')
        return redirect('/cart')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        return redirect('/home')
    if request.method == 'POST':
        requested_items = item_mapper.get_items_from_tuple(request.form)
        valid_loan_state = user_mapper.validate_loan(user_id, len(requested_items))
        if valid_loan_state[0] is True:
            if valid_loan_state[1] is True:
                loaned_items = item_mapper.loan_items(user_id, requested_items)
                if loaned_items is not None:
                    user_mapper.loan_items(user_id, loaned_items)
                    transaction_mapper.add_transactions(user_id, loaned_items, "loan", strftime('%Y-%m-%d %H:%M:%S', localtime()))
                if len(loaned_items) == len(requested_items):
                    flash("Items successfully loaned", 'success')
                    return redirect('/borrowed_items')
                else:
                    flash("Some items became unavailable.", "warning")
                    return redirect('/borrowed_items')
            else:
                flash("There was a problem loaning these items at this time, please try again later.", 'warning')
                return redirect('/cart')
        else:
            flash("This transaction would put you over the loan limit.")
            return redirect('/cart')
    else:
        physical_items = []
        for user in user_mapper.user_registry.list_of_users:
            if user.id == user_id:
                physical_items = user.cart

        detailed_items = item_mapper.get_item_details(physical_items)
        return render_template('cart.html', cart=zip(physical_items, detailed_items))
    return render_template('cart.html')


@app.route('/about')
def about_default():
    return render_template('about.html')

@app.route('/about/<view>')
def about(view):
    if view == 'admin':
        if session['logged_in']:
            if user_mapper.validate_admin(session['user_id'], session['admin']):
                return render_template('about.html', view ="admin")
    elif view == 'client':
        if session['logged_in'] and session['admin'] == 0:
            return render_template('about.html', view="client")

    else:
        return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        user = user_mapper.get_user_by_email(email)
        if user:
            if sha256_crypt.verify(password_candidate, user.password):
                # log user out if they are already logged in
                user_mapper.ensure_not_already_logged(user.id)
                app.logger.info('PASSWORD MATCHED')
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                session['logged_in'] = True
                session['first_name'] = user.first_name
                session['user_id'] = user.id
                session['admin'] = user.admin
                session['timestamp'] = timestamp
                session.permanent = True
                app.permanent_session_lifetime = datetime.timedelta(days=30)

            # add the user to the active user registry in the form of a tuple (user_id, timestamp)
                user_mapper.enlist_active_user(user.id, user.first_name, user.last_name, user.email, user.admin, timestamp, time.time(), time.time(), False)

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


@app.route('/borrowed_items', methods=['GET', 'POST'])
def borrowed_items():
    if session.get('user_id') is not None:
        user_id = session['user_id']
    else:
        return redirect('/home')
    if request.method == 'POST':
        valid_return_state = user_mapper.validate_return()
        if valid_return_state is True:
            physical_items = item_mapper.get_physical_items_from_tuple(request.form)
            item_mapper.return_items(physical_items)
            user_mapper.remove_borrowed_items(user_id, physical_items)
            transaction_mapper.add_transactions(user_id, physical_items, "return", strftime('%Y-%m-%d %H:%M:%S', localtime()))
            flash("Items were successfully returned.", 'success')
            return render_template('home.html', item_list=item_mapper.get_all_items("bb", user_mapper.get_user_cart(user_id)), item="bb")
        else:
            flash("There was an problem returning your items, please try again later.", 'warning')
            return redirect('/borrowed_items')
    else:
        physical_items = []
        for user in user_mapper.user_registry.list_of_users:
            if user.id == user_id:
                physical_items = user.borrowed_items

        detailed_items = item_mapper.get_item_details(physical_items)
        return render_template('borrowed_items.html', borrowed_items=zip(physical_items, detailed_items))


def add_book(request_):
    form = BookForm(request_.form)
    form.all_items = item_mapper.get_all_isbn_items()
    if request_.method == 'POST' and form.validate():
        item_mapper.add_book(form)
        flash('Book is ready to be added - save changes', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_book', form=form)


def add_magazine(request_):
    form = MagazineForm(request_.form)
    form.all_items = item_mapper.get_all_isbn_items()
    if request_.method == 'POST' and form.validate():
        item_mapper.add_magazine(form)
        flash('Magazine is ready to be added - save changes', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_magazine', form=form)


def add_movie(request_):
    form = MovieForm(request_.form)
    if request_.method == 'POST' and form.validate():
        item_mapper.add_movie(form)
        flash('Movie is ready to be added - save changes', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_movie', form=form)


def add_music(request_):
    form = MusicForm(request_.form)
    if request_.method == 'POST' and form.validate():
        item_mapper.add_music(form)
        flash('Music is ready to be added - save changes', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item='add_music', form=form)


@app.route('/admin_tools')
def admin_tools_default():
    if session['logged_in']:
        if user_mapper.validate_admin(session['user_id'], session['admin']):
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('home'))


@app.route('/admin_tools/<tool>', methods=['GET', 'POST'])
def admin_tools(tool):
    if session['logged_in']:
        if user_mapper.validate_admin(session['user_id'], session['admin']):
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry=user_mapper.get_active_users(), tool=tool)
            elif tool == 'create_admin' or tool == 'create_client':
                return user_mapper.register(request, tool)
            elif tool == 'catalog_manager':
                locker = user_mapper.user_registry.check_lock()
                if locker == -1 or locker == session['user_id']:
                    user_mapper.user_registry.lock(session['user_id'])
                    locker = session['user_id']
                    for user in user_mapper.user_registry.active_user_registry:
                        if user[0] == locker and not user[8]:
                            user_as_list = list(user)
                            user_as_list[7] = time.time()
                            user_as_list[8] = True
                            user_mapper.remove_from_active(session['user_id'])
                            user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
                    return render_template('admin_tools.html', tool=tool, catalog=item_mapper.get_catalog(), saved_changes=item_mapper.get_saved_changes())
                else:
                    flash("Catalog currently locked by ID#: " + str(locker) + ".", 'warning')
                    return redirect(url_for('admin_tools_default'))
            elif tool == 'view_users':
                return render_template('admin_tools.html', tool=tool, list_of_users=user_mapper.get_all_users())
            elif tool == 'view_transaction_history':
                return render_template('admin_tools.html', tool=tool, transaction=transaction_mapper.transaction_registry.historical_registry)
            elif tool == 'view_active_loans':
                return render_template('admin_tools.html', tool=tool, transaction=transaction_mapper.transaction_registry.active_loan_registry)
        else:
            flash('invalid tool')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('login'))


@app.route('/admin_tools/edit_entry/<item_prefix>/<item_id>', methods=['GET', 'POST'])
def edit_entry(item_prefix, item_id):
    # Obtain selected item from catalog
    item_selected = item_mapper.find(item_prefix, item_id)

    # the Forms class has a getFormForItemType() which creates a form for the item type selected
    form = Forms.get_form_for_item_type(item_selected.prefix, request.form)
    if request.method == 'POST':
        if item_prefix == 'bb' or item_prefix == 'ma':
            form.all_items = item_mapper.get_all_isbn_items()
            for item in form.all_items:
                if item.id == int(item_id) and item.prefix == item_prefix:
                    form.all_items.remove(item)
        if form.validate():
            physical_items_added = request.form.get("physical_items_added")
            physical_items_removed = request.form.getlist("physical_items_removed")
            item_mapper.set_item(item_prefix, item_id, form, physical_items_added, physical_items_removed)
            return redirect('/admin_tools/catalog_manager')
        else:
            form.quantity.render_kw = {'readonly': 'readonly'}
            return render_template('admin_tools.html', form=form, prefix=item_selected.prefix, id=item_selected.id,
                                   item="edit", copies=item_selected.copies)
    else:

        # Forms class has a getFormData() which returns a preloaded form with the data of the selected item
        form = Forms.get_form_data(item_selected, request)
        form.quantity.render_kw = {'readonly': 'readonly'}
        return render_template('admin_tools.html', form=form, prefix=item_selected.prefix, id=item_selected.id,
                               item="edit", copies=item_selected.copies)


@app.route('/admin_tools/delete_entry/<item_prefix>/<item_id>', methods=['POST'])
def delete_item(item_prefix, item_id):
    delete_success = item_mapper.delete_item(item_prefix, item_id)
    if delete_success:
        flash(f'Item (id {item_prefix} {item_id}) is ready to be deleted. - save changes', 'success')
        return redirect(url_for('admin_tools', tool='catalog_manager'))
    else:
        flash('Item not found.')
        return redirect(url_for('admin_tools', tool='catalog_manager'))


@app.route('/admin_tools/delete_entry/cancel/<item_prefix>/<item_id>', methods=['POST'])
def cancel_deletion(item_prefix, item_id):
    cancel_success = item_mapper.cancel_deletion(item_prefix, item_id)
    if cancel_success:
        flash(f'Item (id {item_prefix} {item_id}) will not be deleted.', 'success')
        return redirect(url_for('admin_tools', tool='catalog_manager'))
    else:
        flash('Item not found.')
        return redirect(url_for('admin_tools', tool='catalog_manager'))


@app.route('/admin_tools/catalog_manager/<item>', methods=['GET', 'POST'])
def catalog_manager(item):
    if session['logged_in']:
        if user_mapper.validate_admin(session['user_id'], session['admin']):
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


@app.route('/admin_tools/catalog_manager/commit', methods=['POST'])
def save_changes():
    item_mapper.end()
    flash('All changes have been saved')
    return redirect(url_for('admin_tools', tool='catalog_manager'))


@app.route('/logout')
def logout():
    user_mapper.remove_from_active(session['user_id'])
    locker = user_mapper.user_registry.check_lock()
    if locker == session['user_id']:
        user_mapper.user_registry.remove_lock()
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
