from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from domain.system import System
from domain.db import db
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from model.RegisterForm import RegisterForm

app = Flask(__name__)

appdb = db(app)

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

        client = appdb.getClientByEmail(email)

        if client:

            #compare passwrods
            if sha256_crypt.verify(password_candidate, client.password):
                app.logger.info('PASSWORD MATHCED')
                session['logged_in'] = True
                session['firstname'] = client.firstname

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

        appdb.insertClient(form.firstname.data, form.lastname.data, form.address.data, form.email.data, form.phone.data, sha256_crypt.encrypt(str(form.password.data)))

        flash('You are now registered and can now login', 'success')

        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)