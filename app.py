from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.User import User, Client, Admin, active_user_registry
from model.Catalog import Catalog
from model.Item import Item, Book, Magazine, Movie, Music
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from model.RegisterForm import RegisterForm
from model.ItemForm import ItemForm
from model.AddBook import BookForm
from model.AddMagazine import MagazineForm
from model.AddMovie import MovieForm
from model.AddMusic import MusicForm
import datetime, time

app = Flask(__name__)
tdg = Tdg(app)
global catalog
catalog = Catalog()

item1 = Book("Neuromancer", "bb", 1, "avail", "William Gibson", "paperback", 273, "CD Projekt Red", "English", 1337187420, 1337187420666)
item2 = Magazine("Science", "ma", 2, "torn", "Science people", "Sciencish", 1337187420, 1337187420666)
item3 = Movie("One Flew Over the Cuckoo's Nest", "mo", 3, "watched", "Kubrick?", "Uhh...", "Jack Nicholson!", "English", "none", "nope", 1973, 180)
item4 = Music("Hafanana", "mu", 4, "loaned", "CD", "Valeri Leontiev", "CCCP", 1986, 123456)
catalog.item_catalog = [item1, item2, item3, item4]

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

        data = tdg.getClientByEmail(email)
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    app.logger.info(form.phone.data)
    if request.method == 'POST' and form.validate():
        if not (tdg.getClientByEmail(form.email.data)):

            is_admin = 0
            tdg.insertClient(form.firstname.data, form.lastname.data, form.address.data, form.email.data, form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))

            flash('You are now registered and can now login', 'success')

            return redirect(url_for('index'))

        flash("This email has already been used.")
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)

def register_admin(request):
    form = RegisterForm(request.form)
    app.logger.info(form.phone.data)
    if request.method == 'POST' and form.validate():
        if not (tdg.getClientByEmail(form.email.data)):
            is_admin = 1
            tdg.insertClient(form.firstname.data, form.lastname.data, form.address.data, form.email.data, form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))

            flash('The new administrator has been registered', 'success')

            return redirect(url_for('admin_tools_default'))
        
        else:
            flash("This email has already been used.")
            return render_template('admin_tools.html', tool='create_admin', form=form)

    return render_template('admin_tools.html', tool = 'create_admin', form=form)

def add_book(request):
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Book", form)
        flash('Book was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        flash('Invalid book item to add')
        return render_template('admin_tools.html', item = 'add_book', form=form)

def add_magazine(request):
    form = MagazineForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Magazine", form)
        flash('Magazine was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        flash('Invalid magazine item to add')
        return render_template('admin_tools.html', item = 'add_magazine', form=form)

def add_movie(request):
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Movie", form)
        flash('Movie was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        flash('Invalid movie item to add')
        return render_template('admin_tools.html', item = 'add_movie', form=form)

def add_music(request):
    form = MusicForm(request.form)
    if request.method == 'POST' and form.validate():
        catalog.add_item("Music", form)
        flash('Music was successfully added', 'success')
        return redirect('/admin_tools/catalog_manager')
    else:
        flash('Invalid music item to add')
        return render_template('admin_tools.html', item = 'add_music', form=form)

@app.route('/admin_tools')
def admin_tools_default():
    if session['logged_in'] == True:
        if Admin.validate_admin(active_user_registry, session['client_id'], session['admin']):
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page')
    return redirect(url_for('home'))


@app.route('/admin_tools/<tool>',  methods=['GET', 'POST'])
def admin_tools(tool):
    if session['logged_in'] == True:
        if Admin.validate_admin(active_user_registry, session['client_id'], session['admin']):
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry = active_user_registry, tool = tool)
            elif tool == 'create_admin':
                return register_admin(request)
            elif tool == 'catalog_manager':
                return render_template('admin_tools.html', tool = tool, catalog = catalog)

            # elif tool == 'some_future_tool':
        else:
            flash('invalid tool')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page')
    return redirect(url_for('login'))

@app.route('/admin_tools/edit_entry/<id>',  methods=['GET', 'POST'])
def edit_entry(id):

    # Todo : Determine which type of item was selected and load the appropriate type of form
    # The following applies only to the Book item

    itemSelected = catalog.getItemById(id)
    form = ItemForm(request.form)
    if itemSelected.prefix == 'bb':
        form.title.data = itemSelected.title
        form.author.data = itemSelected.author
        form.format.data = itemSelected.format
        form.pages.data = itemSelected.pages
        form.publisher.data = itemSelected.publisher
        form.language.data = itemSelected.language
        form.isbn10.data = itemSelected.isbn10
        form.isbn13.data = itemSelected.isbn13
    if itemSelected.prefix == 'ma':
        form.title.data = itemSelected.title
        form.publisher.data = itemSelected.publisher
        form.language.data = itemSelected.language
        form.isbn10.data = itemSelected.isbn10
        form.isbn13.data = itemSelected.isbn13
    if itemSelected.prefix == 'mo':
        form.title.data = itemSelected.title
        form.director.data = itemSelected.director
        form.producers.data = itemSelected.producers
        form.actors.data = itemSelected.actors
        form.language.data = itemSelected.language
        form.subtitles.data = itemSelected.subtitles
        form.dubbed.data = itemSelected.dubbed
        form.releaseDate.data = itemSelected.releaseDate
        form.runTime.data = itemSelected.runTime
    if itemSelected.prefix == 'mu':
        form.musicType.data = itemSelected.musicType
        form.title.data = itemSelected.title
        form.artist.data = itemSelected.artist
        form.label.data = itemSelected.label
        form.releaseDate.data = itemSelected.releaseDate
        form.asin.data = itemSelected.asin

    return render_template('edit_page.html', form=form, prefix = itemSelected.prefix, id = itemSelected.id)

@app.route('/admin_tools/delete_entry/<id>',  methods=['GET', 'POST'])
def delete_entry(id):
    catalog.delete_item()
    return render_template('admin_tools.html')

@app.route('/admin_tools/modify/<id>',  methods=['GET', 'POST'])
def modify(id):
    catalog.edit_item(request.form, id)
    return render_template('admin_tools.html')


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