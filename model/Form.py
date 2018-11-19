from wtforms import ValidationError, Form, StringField, PasswordField, validators, IntegerField, SelectField
import datetime
import re


def alpha(minimum, maximum, allow_digits):
    def _alpha(form, field):
        length = len(field.data)
        if length < minimum or length > maximum:
            raise ValidationError('Input length must be between %d and %d characters long.' % (minimum, maximum))
        if allow_digits == 0:
            if any(char.isdigit() for char in field.data):
                raise ValidationError('Input must not contain any digits.')
    return _alpha


def num(minimum, maximum):
    def num(form, field):
        if field.data == '' or not all(char.isdigit() for char in field.data):
            raise ValidationError('Input must be a valid digit.')
        data = int(field.data)
        if data < minimum or data > maximum:
            raise ValidationError('Input value must be between %d and %d.' % (minimum, maximum))
    return num


def password(form, field):
    minimum_password_length = 6
    if type(field.data) is str:
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least 1 digit.')
        elif not any(char.isalpha() for char in field.data):
            raise ValidationError('Password must contain at least 1 letter.')
    elif len(field.data) < minimum_password_length:
        raise ValidationError('The password needs to be at least ' + str(minimum_password_length) + ' characters.')


# Verifies phone number does not contain any letter
def phone_number(form, field):
    if len(field.data) == 0:
        raise ValidationError('Please enter a phone number.')
    elif not re.match('^[(]\d{3}[)]\s*\d{3}[-]\d{4}$', field.data):
        raise ValidationError('Invalid phone number, please follow the pattern: (514) 423-3918')


# Verifies that the date input matches the format DD-MM-YYYY
def date(form, field):
    try:
        datetime.datetime.strptime(field.data, "%Y-%m-%d")
    except ValueError:
        raise ValueError("The date must be formatted as follows: YYYY-MM-DD.")


def unique_email_validator(form, field):
        for user in form.all_users:
            if form.email.data == user.email and not form.user[0] == user.id:
                raise ValidationError('This email has already been used by user id' + str(user.id) + " and can't be used by user id " + str(form.user[0]) + '.')


def unique_isbn10_validator(form, field):
    if field.data == '' or not all(char.isdigit() for char in field.data):
        raise ValidationError('Input must be a valid digit.')
    data = int(field.data)
    if data < 1000000000 or data > 9999999999:
        raise ValidationError('Please enter a valid 10-digit ISBN number.')
    for item in form.all_items:
        if int(form.isbn10.data) == item.isbn10:
            raise ValidationError("Duplicate ISBN - " + item.prefix + " ID#: " + str(item.id) + ", Title: " + item.title + ", ISBN10: " + str(item.isbn10))


def unique_isbn13_validator(form, field):
    if field.data == '' or not all(char.isdigit() for char in field.data):
        raise ValidationError('Input must be a valid digit.')
    data = int(field.data)
    if data < 1000000000000 or data > 9999999999999:
        raise ValidationError('Please enter a valid 13-digit ISBN number.')
    for item in form.all_items:
        if int(form.isbn13.data) == item.isbn13:
            raise ValidationError("Duplicate ISBN - " + item.prefix + " ID#: " + str(item.id) + ", Title: " + item.title + ", ISBN13: " + str(item.isbn13))


class RegisterForm(Form):
    first_name = StringField('First Name', [alpha(2, 50, 0)])
    last_name = StringField('Last Name', [alpha(2, 50, 0)])
    email = StringField('Email', [validators.Email(message='This is not a valid email address.')])
    phone = StringField('Phone', [phone_number])
    address = StringField('Address', [alpha(2, 100, 1)])
    password = PasswordField('Password', [
        password,
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirmed Password')


class EditForm(Form):
    first_name = StringField('First Name', [alpha(2, 50, 0)])
    last_name = StringField('Last Name', [alpha(2, 50, 0)])
    email = StringField('Email', [validators.Email(message='This is not a valid email address.'), unique_email_validator])
    phone = StringField('Phone', [phone_number])
    address = StringField('Address', [alpha(2, 100, 1)])


class PasswordForm(Form):
    password = PasswordField('Password', [
        password,
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirmed Password')


class BookForm(Form):
    current_time = datetime.datetime.now()
    title = StringField('Title', [alpha(1, 100, 1)])
    author = StringField('Author', [alpha(5, 100, 0)])
    format = SelectField('Format', choices=[('Paperback', 'Paperback'), ('Hardcover', 'Hardcover')])
    publication_year = StringField('Publication Year', [num(0, current_time.year)])
    pages = StringField('Pages', [num(1, 99999)])
    publisher = StringField('Publisher', [alpha(1, 100, 1)])
    language = StringField('Language', [alpha(1, 100, 0)])
    isbn10 = StringField('ISBN10', [unique_isbn10_validator])
    isbn13 = StringField('ISBN13', [unique_isbn13_validator])
    quantity = StringField('Quantity', [num(0, 255)])


class MagazineForm(Form):
    title = StringField('Title', [alpha(1, 100, 1)])
    publisher = StringField('Publisher', [alpha(1, 100, 1)])
    publication_date = StringField('Publication Date', [date])
    language = StringField('Language', [alpha(1, 100, 0)])
    isbn10 = StringField('ISBN10', [unique_isbn10_validator])
    isbn13 = StringField('ISBN13', [unique_isbn13_validator])
    quantity = StringField('Quantity', [num(0, 255)])


class MovieForm(Form):
    title = StringField('Title', [alpha(1, 100, 1)])
    director = StringField('Director', [alpha(5, 100, 0)])
    producers = StringField('Producers', [alpha(5, 100, 0)])
    actors = StringField('Actors', [alpha(5, 100, 0)])
    language = StringField('Language', [alpha(1, 100, 0)])
    subtitles = StringField('Subtitles', [alpha(1, 100, 0)])
    dubbed = StringField('Dubbed', [alpha(0, 100, 0)])
    release_date = StringField('Release Date', [date])
    runtime = StringField('Run Time ', [alpha(2, 50, 1)])
    quantity = StringField('Quantity', [num(0, 255)])


class MusicForm(Form):
    media_type = StringField('Type', [alpha(2, 100, 0)])
    title = StringField('Title', [alpha(1, 100, 1)])
    artist = StringField('Artist', [alpha(1, 100, 1)])
    label = StringField('Label', [alpha(1, 100, 1)])
    release_date = StringField('Release Date', [date])
    asin = StringField('ASIN', [alpha(10, 10, 1)])
    quantity = StringField('Quantity', [num(0, 255)])


class SearchForm(Form):
    filter = StringField('Filter')
    search = StringField('Search')


class OrderForm(Form):
    order_filter = StringField('Order Filter')
    order_type = StringField('Order Type')


class Forms(Form):

    @staticmethod
    def get_form_for_item_type(item_type, form):
        if item_type == 'bb':
            return BookForm(form)
        elif item_type == 'ma':
            return MagazineForm(form)
        elif item_type == 'mo':
            return MovieForm(form)
        elif item_type == "mu":
            return MusicForm(form)
        else:
            return None

    @staticmethod
    def get_form_data(item_selected, request):
        selected_item_type = item_selected.prefix
        form = None
        if selected_item_type == 'bb':
            form = BookForm(request.form)
            form.title.data = item_selected.title
            form.author.data = item_selected.author
            form.format.data = item_selected.format
            form.publication_year.data = item_selected.publication_year
            form.pages.data = item_selected.pages
            form.publisher.data = item_selected.publisher
            form.publication_year.data = item_selected.publication_year
            form.language.data = item_selected.language
            form.isbn10.data = item_selected.isbn10
            form.isbn13.data = item_selected.isbn13
            form.quantity.data = item_selected.quantity

        elif selected_item_type == 'ma':
            form = MagazineForm(request.form)
            form.title.data = item_selected.title
            form.publisher.data = item_selected.publisher
            form.publication_date.data = item_selected.publication_date
            form.language.data = item_selected.language
            form.isbn10.data = item_selected.isbn10
            form.isbn13.data = item_selected.isbn13
            form.quantity.data = item_selected.quantity

        elif selected_item_type == 'mo':
            form = MovieForm(request.form)
            form.title.data = item_selected.title
            form.director.data = item_selected.director
            form.producers.data = item_selected.producers
            form.actors.data = item_selected.actors
            form.language.data = item_selected.language
            form.subtitles.data = item_selected.subtitles
            form.dubbed.data = item_selected.dubbed
            form.release_date.data = item_selected.release_date
            form.runtime.data = item_selected.runtime
            form.quantity.data = item_selected.quantity

        elif selected_item_type == 'mu':
            form = MusicForm(request.form)
            form.title.data = item_selected.title
            form.media_type.data = item_selected.media_type
            form.artist.data = item_selected.artist
            form.label.data = item_selected.label
            form.release_date.data = item_selected.release_date
            form.asin.data = item_selected.asin
            form.quantity.data = item_selected.quantity

        return form

    @staticmethod
    def get_user_form_data(user_selected, request):

        form = EditForm(request.form)
        form.first_name.data = user_selected[1]
        form.last_name.data = user_selected[2]
        form.address.data = user_selected[3]
        form.email.data = user_selected[4]
        form.phone.data = user_selected[5]

        return form
