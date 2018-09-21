from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from domain.system import System
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

ourSystem = System('version1')

mysql = MySQL()

# Config MySQL
app.config['MYSQL_DATABASE_USER'] = 'pomoroad_soen09'
app.config['MYSQL_DATABASE_PASSWORD'] = 'discordApp343'
app.config['MYSQL_DATABASE_DB'] = 'pomoroad_soen343'
app.config['MYSQL_DATABASE_HOST'] = '108.167.160.63'


# init MYSQL
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('home.html', sysObj = ourSystem)

@app.route('/home')
def home():
    return render_template('home.html', sysObj = ourSystem)

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=50)])
    lastname = StringField('Last Name', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    phone = StringField('Phone', [validators.Length(min=1, max=12)])
    address = StringField('Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirmed Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        #Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        connection = mysql.connect()
        cur = connection.cursor()

        result = cur.execute("SELECT * FROM clientAdmin WHERE email = %s", [email])

        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data[7]
            firstname = data[1]
            app.logger.info(password)

            #compare passwrods
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATHCED')
                session['logged_in'] = True
                session['firstname'] = firstname

                flash('You are now logged in', 'success')
                return redirect(url_for('home'))
                
            else:
                error = 'Invalid login'
                app.logger.info('NOT MATCHED')
                return render_template('login.html', error=error, form=form)
            cur.close()
        else:
            app.logger.info('NO USER')
            error = 'Email not found'
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        address = form.address.data
        phone = form.phone.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        connection = mysql.connect()
        cur = connection.cursor()

        # Execute query
        cur.execute("INSERT INTO clientAdmin(id, firstName, lastName, physicalAddress, email, phone, admin, password) VALUES(NULL, %s, %s, %s, %s, %s, 0, %s)", (firstname, lastname, address, email, phone, password))
        # Close connection
        cur.close()

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