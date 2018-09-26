from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.db import db
from model.Client import Client
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from model.RegisterForm import RegisterForm
import datetime

app = Flask(__name__)

appdb = db(app)

active_user_registry = []

def validate_admin():
    for client in active_user_registry:
        if client.id == session['client_id'] and client.admin == True:
            return True
    return False

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

        data = appdb.getClientByEmail(email)
        if data:
            client = Client(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            # add the client to the active user registry in the form of a tuple (id, timestamp)
            ts = datetime.datetime.now().timestamp
            active_user_registry.append(data[0],ts)

            #compare passwrods
            if sha256_crypt.verify(password_candidate, client.password):
                app.logger.info('PASSWORD MATHCED')
                session['logged_in'] = True
                session['firstname'] = client.firstname
                session['client_id'] = client.id

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
    app.logger.info(form.firstname.data)
    if request.method == 'POST' and form.validate():
        is_admin = 0
        appdb.insertClient(form.firstname.data, form.lastname.data, form.address.data, form.email.data, form.phone.data, is_admin, sha256_crypt.encrypt(str(form.password.data)))

        flash('You are now registered and can now login', 'success')

        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    # TODO 
    return

@app.route('/admin_tools')
def admin_tools_default():
    if session['logged_in'] == True:
        if validate_admin():
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page')
    return redirect(url_for('login'))

@app.route('/admin_tools/<tool>')
def admin_tools(tool):
    if session['logged_in'] == True:
        if validate_admin():
            if tool == 'view_active_registry':
                return render_template('admin_tools.html', active_user_registry = active_user_registry)
            # elif tool == 'some_future_tool':
        else:
            flash('invalid tool')
            return render_template('admin_tools.html')
    flash('You must be logged in as an admin to view this page')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove client from the active_user_registry
    # to verify (not sure about the syntax here) - will be updated to reflect removal of tuple
    active_user_registry[:] = [client for client in active_user_registry if not client.id == session['client_id']]
    session.clear()

    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)