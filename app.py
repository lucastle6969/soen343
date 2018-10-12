from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.User import User, Client, Admin, active_user_registry
from model.Catalog import Catalog
from model.Item import Item, Book, Magazine, Movie, Music
from passlib.hash import sha256_crypt
from model.RegisterForm import RegisterForm
from model.AddBook import BookForm
from model.AddMagazine import MagazineForm
from model.AddMovie import MovieForm
from model.AddMusic import MusicForm
import datetime, time

app = Flask(__name__)
tdg = Tdg(app)
global catalog
catalog = Catalog()

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
        #Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        data = tdg.getUserByEmail(email)
        if data:
            id = data[0]
            firstname = data[1]
            lastname = data[2]
            address = data[3]
            email = data[4]
            phone = data[5]
            admin = data[6]
            password = data[7]

            client = Client(id, firstname, lastname, address, email, phone, admin, password)
            # log user out if they are already logged in
            active_user_registry[:] = [tup for tup in active_user_registry if not data[0]==tup[0]]
            # add the client to the active user registry in the form of a tuple (id, timestamp)
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            active_user_registry.append((data[0],timestamp))

            #compare passwrods
            if sha256_crypt.verify(password_candidate, client.password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['firstname'] = client.firstname
                session['client_id'] = client.id
                session['admin'] = client.admin

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

def register(request, tool):
    form = RegisterForm(request.form)
    app.logger.info(tool)
    if request.method == 'POST' and form.validate():
        if not (tdg.getUserByEmail(form.email.data)):
            if (tool == 'create_admin'):
                is_admin = 1
            if (tool == 'create_client'):
                is_admin = 0
            
            tdg.insertUser(form.firstname.data, form.lastname.data, form.address.data, form.email.data, form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))
            
            if (tool == 'create_admin'):
                flash('The new administrator has been registered', 'success')
            if (tool == 'create_client'):
                flash('The new client has been registered', 'success')

            return redirect(url_for('admin_tools_default'))
        
        else:
            flash("This email has already been used.")
            return render_template('admin_tools.html', tool='create_admin', form=form)

    return render_template('admin_tools.html', tool=tool, form=form)

def add_book(request):
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Book", form)
        flash('Book was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item = 'add_book', form=form)

def add_magazine(request):
    form = MagazineForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Magazine", form)
        flash('Magazine was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item = 'add_magazine', form=form)

def add_movie(request):
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Movie", form)
        flash('Movie was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item = 'add_movie', form=form)

def add_music(request):
    form = MusicForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Music", form)
        flash('Music was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        return render_template('admin_tools.html', item = 'add_music', form=form)

@app.route('/admin_tools')
def admin_tools_default():
    if session['logged_in'] == True:
        if Admin.validate_admin(active_user_registry, session['client_id'], session['admin']):
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('home'))

@app.route('/admin_tools/<tool>',  methods=['GET', 'POST'])
def admin_tools(tool):
    if session['logged_in'] == True:
        if Admin.validate_admin(active_user_registry, session['client_id'], session['admin']):
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry = active_user_registry, tool = tool)
            elif tool == 'create_admin' or tool == 'create_client':
                return register(request, tool)
            elif tool == 'catalog_manager':
                return render_template('admin_tools.html', tool = tool, catalog = catalog)
            elif tool == 'view_users':
                list_of_users = tdg.getAllUsers()
                return render_template('admin_tools.html', tool = tool, list_of_users = list_of_users)
        else:
            flash('invalid tool')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page.')
    return redirect(url_for('login'))

@app.route('/admin_tools/edit_entry/<id>',  methods=['GET', 'POST'])
def edit_entry(id):
    # Obtain selected item from catalog
    itemSelected = catalog.getItemById(id)
    seletedItemType = itemSelected.prefix

    # getFormForItemType() creates a form for the item type selected
    form = catalog.getFormForItemType(seletedItemType, request.form)

    if request.method == 'POST': # TODO: Add form.validate() before adding to catalog
        catalog.edit_item(id, form)
        return redirect('/admin_tools/catalog_manager')
    else:
        # getFormData() returns a preloaded form with the data of the selected item
        form = catalog.getFormData(itemSelected, request)
        return render_template('edit_page.html', form=form, prefix = seletedItemType, id = itemSelected.id)

@app.route('/admin_tools/delete_entry/<id>',  methods=['POST'])
def delete_item(id):
    delete_success = catalog.delete_item(id)
    if(delete_success):
        flash(f'Item (id {id}) deleted.', 'success')
        return redirect(url_for('admin_tools', tool='catalog_manager'))
    else:
        flash('Item not found.')
        return redirect(url_for('admin_tools', tool='catalog_manager'))

@app.route('/admin_tools/catalog_manager/<item>',  methods=['GET', 'POST'])
def catalog_manager(item):
    app.logger.info(item)
    if session['logged_in'] == True:
        if Admin.validate_admin(active_user_registry, session['client_id'], session['admin']):
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
    # Remove client_id, timestamp tuple from the active_user_registry
    active_user_registry[:] = [tup for tup in active_user_registry if not session['client_id']==tup[0]]
    session.clear()

    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)