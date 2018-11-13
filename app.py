from flask import Flask, render_template, flash, redirect, url_for, session, request
from model.ItemMapper import ItemMapper
from model.UserMapper import UserMapper
from passlib.hash import sha256_crypt
from model.Form import RegisterForm, BookForm, MagazineForm, MovieForm, MusicForm, SearchForm, Forms
import datetime
import time

app = Flask(__name__)
item_mapper = ItemMapper(app)
user_mapper = UserMapper(app)


@app.before_request
def before_request():
    if len(session) > 0 and not (len(session) == 1 and '_flashes' in session):
        user_id = session['user_id']
        for user in user_mapper.user_registry.active_user_registry:
            if user[0] == user_id:
                if time.time() - user[6] > 10:
                    user_mapper.remove_from_active(session['user_id'])
                    session.clear()
                    flash('Automatically logged out due to timeout.', 'warning')
                    return redirect(url_for('home'))
                else:
                    user_as_list = list(user)
                    user_as_list[6] = time.time()
                    user_mapper.remove_from_active(session['user_id'])
                    user_mapper.user_registry.active_user_registry.append(tuple(user_as_list))
    cleared = user_mapper.check_restart_session(session)
    if cleared:
        flash('Automatically logged out due to a disconnect', 'warning')
        return redirect(url_for('home'))




@app.route('/')
def index():
    # Default table view shows all books
    return render_template('home.html', item_list=item_mapper.get_all_items("bb"), item="bb")


@app.route('/home')
def home():
    # Default table view shows all books
    return render_template('home.html', item_list=item_mapper.get_all_items("bb"), item="bb")


@app.route('/home/<item>')
def itemList(item):
    if item == "bb":
        return render_template('home.html', item_list=item_mapper.get_all_items("bb"), item="bb")
    elif item == "ma":
        return render_template('home.html', item_list=item_mapper.get_all_items("ma"), item="ma")
    elif item == "mu":
        return render_template('home.html', item_list=item_mapper.get_all_items("mu"), item="mu")
    elif item == "mo":
        return render_template('home.html', item_list=item_mapper.get_all_items("mo"), item="mo")


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
        user = user_mapper.get_user_by_email(email)
        if user:
            if sha256_crypt.verify(password_candidate, user.password):
                # log user out if they are already logged in
                user_mapper.ensure_not_already_logged(user.id)
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['first_name'] = user.first_name
                session['user_id'] = user.id
                session['admin'] = user.admin

            # add the user to the active user registry in the form of a tuple (user_id, timestamp)
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

                user_mapper.enlist_active_user(user.id, user.first_name, user.last_name, user.email, user.admin, timestamp, time.time())
                if user_mapper.check_another_admin(user.id):
                    flash('Limited functionality', 'warning')
                    return redirect(url_for('home'))

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
        if user_mapper.validate_admin(session['user_id'], session['admin']) and not user_mapper.check_another_admin(int(session['user_id'])):
            return render_template('admin_tools.html')
        flash("Limited functionality, cannot modify catalog.", "warning")
        return render_template('admin_tools.html', limited='limited')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('home'))


@app.route('/admin_tools/<tool>',  methods=['GET', 'POST'])
def admin_tools(tool):
    if session['logged_in']:
        if user_mapper.validate_admin(session['user_id'], session['admin']):
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry=user_mapper.get_active_users(), tool=tool)
            elif tool == 'create_admin' or tool == 'create_client':
                return user_mapper.register(request, tool)
            elif tool == 'catalog_manager':
                return render_template('admin_tools.html', tool=tool, catalog=item_mapper.get_catalog(), saved_changes=item_mapper.get_saved_changes())
            elif tool == 'catalog_manager_limited':
                return render_template('admin_tools.html', tool=tool, catalog=item_mapper.get_catalog())
            elif tool == 'view_users':
                return render_template('admin_tools.html', tool=tool, list_of_users=user_mapper.get_all_users())
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
            item_mapper.set_item(item_prefix, item_id, form)
            return redirect('/admin_tools/catalog_manager')
        else:
            form.quantity.render_kw = {'readonly': 'readonly'}
            return render_template('admin_tools.html', form=form, prefix=item_selected.prefix, id=item_selected.id,
                                   item="edit")
    else:

        # Forms class has a getFormData() which returns a preloaded form with the data of the selected item
        form = Forms.get_form_data(item_selected, request)
        form.quantity.render_kw = {'readonly': 'readonly'}
        return render_template('admin_tools.html', form=form, prefix=item_selected.prefix, id=item_selected.id,
                               item="edit")


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


@app.route('/admin_tools/catalog_manager/<item>',  methods=['GET', 'POST'])
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
    session.clear()

    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
