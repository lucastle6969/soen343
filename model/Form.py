from wtforms import ValidationError, Form, StringField, PasswordField, validators, IntegerField
import datetime
import re

def input_required(message):
    def _title(form, field):
        if len(field.data) < 1:
            raise ValidationError(message)  
    
    return _title

def person_name(form, field):
    if len(field.data) == 0:
        raise ValidationError('Please enter the name')  
    elif len(field.data) > 70:
        raise ValidationError('This name is too long to be real')
    elif len(field.data) < 2:
        raise ValidationError('The name is too short to be real') 
    elif any(char.isdigit() for char in field.data):
        raise ValidationError('Must not contain any numerical digit')

# Verifies if password does contain at least a letter and a digit
def password(form, field):
    mininum_password_length = 6
    if type(field.data) is str:
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Must contain at least 1 digit')
        elif not any(char.isalpha() for char in field.data):
            raise ValidationError('Must contain at least 1 letter')
    elif (len(field.data) < mininum_password_length):
        raise ValidationError('The password needs to be at least ' + str(mininum_password_length) + ' characters')


# Verifies phone number does not contain any letter
def phone_number(form, field):
    if false:
        raise ValidationError('it matches!')
    if type(field.data) is not int:
        if type(field.data) is str:
            if any(char.isalpha() for char in field.data):
                raise ValidationError('Phone numbers should not contain any alphabetic character')
    elif len(field.data) < 10:
        raise ValidationError('The phone number needs more digits to be valid')


# Verifies that the date input matches the format DD-MM-YYYY
def date(form, field):
    try:
        datetime.datetime.strptime(field.data, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Must be a date of format DD-MM-YYYY")


# Verifies string does not contain any letter
def number(form, field):
    if type(field.data) is not int:
        if type(field.data) is str:
            if any(char.isalpha() for char in field.data):
                raise ValidationError('A number cannot contain any alphabetic character')
    


# Verifies word does not contain any digit
def no_digit(form, field):
    if type(field.data) is str:
        if any(char.isdigit() for char in field.data):
            raise ValidationError('This field cannot contain any digit')
    else:
        raise ValidationError('This field cannot contain any digit')


def alpha_numeric(form, field):
    if type(field.data) is int:
        raise ValidationError('This field cannot contain only digits')
    elif type(field.data) is str:
        char_count = 0
        if any(char.isalpha() for char in field.data):
            char_count += 1
        if char_count == 0:
            raise ValidationError('This field cannot contain only digits')


class RegisterForm(Form):
    first_name = StringField('First Name', [person_name])
    last_name = StringField('Last Name', [person_name])
    email = StringField('Email', [validators.Email(message='This is not a valid email.')])
    phone = StringField('Phone', [phone_number, validators.Length(min=8, max=15, message='This is not a valid phone number.')])
    address = StringField('Address', [input_required(message='Please enter the home address.')])
    password = PasswordField('Password', [
        password,
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirmed Password')


class BookForm(Form):
    current_time = datetime.datetime.now()
    title = StringField('Title', [input_required(message='Please insert the title of the book.')])
    author = StringField('Author', [person_name, no_digit])
    format = StringField('Format', [alpha_numeric, input_required(message='Please enter the format of the book.')])
    # From the first printed text (Gutenberg Bible in 1455) to this present year
    publication_year = IntegerField('Publication Year', [validators.NumberRange(min=1455, max=current_time.year, message='This is not a valid year for a published book.')])
    pages = IntegerField('Pages', [number, validators.NumberRange(min=1, max=99999, message="That is not a valid number of pages.")])
    publisher = StringField('Publisher', [alpha_numeric, input_required(message='Please enter the name of the publisher.')])
    language = StringField('Language', [no_digit, input_required(message='Please enter the language in which the book is published.')])
    isbn10 = IntegerField('ISBN10', [number, validators.NumberRange(min=1000000000, max=9999999999, message='Please enter a valid 10-digit ISBN.')])
    isbn13 = IntegerField('ISBN13', [number, validators.NumberRange(min=1000000000000, max=9999999999999, message='Please enter a valid 13-digit ISBN.')])
    quantity = IntegerField('Quantity', [input_required(message='Please enter the amount of books to register under this entry.'), number, validators.NumberRange(min=1, max=255)])

class MagazineForm(Form):
    title = StringField('Title', [input_required(message='Please insert the title of the magazine.')])
    publisher = StringField('Publisher', [alpha_numeric, input_required(message='Please enter the name of the publisher.')])
    language = StringField('Language', [no_digit, input_required(message='Please enter the language in which the magazine is published.')])
    isbn10 = IntegerField('ISBN10', [number, validators.NumberRange(min=1000000000, max=9999999999, message='Please enter a valid 10-digit ISBN.')])
    isbn13 = IntegerField('ISBN13', [number, validators.NumberRange(min=1000000000000, max=9999999999999, message='Please enter a valid 13-digit ISBN.')])
    quantity = IntegerField('Quantity', [input_required(message='Please enter the amount of magazines to register under this entry.'), number, validators.NumberRange(min=1, max=255)])


class MovieForm(Form):
    title = StringField('Title', [input_required(message='Please insert the title of the movie.')])
    director = StringField('Director', [no_digit, input_required(message='Please enter the name of the director.')])
    producers = StringField('Producers', [no_digit, input_required(message='Please enter the name of the producer(s).')])
    actors = StringField('Actors', [no_digit, input_required(message='Please enter the name of the actor(s).')])
    language = StringField('Language', [no_digit, input_required(message='Please enter the name of the actor(s).')])
    subtitles = StringField('Subtitles', [no_digit, input_required(message='Please enter the language of the subtitles.')])
    dubbed = StringField('Dubbed', [no_digit])
    release_date = StringField('Release Date', [date])
    runtime = StringField('Run Time ', [number, validators.Length(min=1, max=30)])
    quantity = IntegerField('Quantity', [input_required(message='Please enter the amount of musics to register under this entry.'), number, validators.NumberRange(min=1, max=255)])


class MusicForm(Form):
    media_type = StringField('Type', [validators.Length(min=1, max=5, message="This is not a valid format for a music file.")])
    title = StringField('Title', [input_required(message='Please insert the title of the music.')])
    artist = StringField('Artist', [input_required(message='Please insert the name of the artist.')])
    label = StringField('Label', [input_required(message='Please insert the label of the music.')])
    release_date = StringField('Release Date', [date])
    asin = StringField('ASIN', [validators.Length(min=10, max=10, message='This is not a valid ASIN code.')])
    quantity = IntegerField('Quantity', [input_required(message='Please enter the amount of musics to register under this entry.'), number, validators.NumberRange(min=1, max=255)])

class SearchForm(Form):
    filter = StringField('Filter')
    search = StringField('Search')
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
