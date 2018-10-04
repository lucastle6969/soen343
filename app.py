from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.User import User, Client, Admin, active_user_registry
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from model.RegisterForm import RegisterForm
import datetime, time

app = Flask(__name__)

tdg = Tdg(app)

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
            # elif tool == 'some_future_tool':
        else:
            flash('invalid tool')
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