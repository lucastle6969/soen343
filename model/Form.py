from wtforms import ValidationError, Form, StringField, PasswordField, validators, IntegerField
import datetime


def personName_(form, field):
    if any(char.isdigit() for char in field.data):
        raise ValidationError('Must not contain any numerical digit')
    if len(field.data)==0:
        raise ValidationError('This field is required')
    if len(field.data)>70:
        raise ValidationError('This name is too long to be real')

# Verifies if password does contain at least a letter and a digit
def password_(form, field):
    num:int = 6
    if not any(char.isdigit() for char in field.data):
        raise ValidationError('Must contain at least 1 digit')
    if not any(char.isalpha() for char in field.data):
        raise ValidationError('Must contain at least 1 letter')
    if (len(field.data) < num):
        raise ValidationError('The password needs to be at least '+num+' characters')

# Verifies phone number does not contain any letter
def phone_number_(form, field):
    if any(char.isalpha() for char in field.data):
        raise ValidationError('Phone numbers do not contain any alphabetic character')

# Verifies that the date input matches the format DD-MM-YYYY
def date(form, field):
    try:
        datetime.datetime.strptime(field.data, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Must be a date of format DD-MM-YYYY")

# Verifies string does not contain any letter
def number(form, field):
    if any(char.isalpha() for char in field.data):
        raise ValidationError('A number cannot contain any alphabetic character')

# Verifies word does not contain any digit
def noDigit(form, field):
    if any(char.isdigit() for char in field.data):
        raise ValidationError('This field cannot contain any digit')


class RegisterForm(Form):
    firstname = StringField('First Name', [validators.DataRequired(), personName_])
    lastname = StringField('Last Name', [validators.DataRequired(), personName_])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    phone = StringField('Phone', [validators.DataRequired(), phone_number_,validators.Length(min=1, max=12)])
    address = StringField('Address', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(), 
        password_,
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirmed Password')


class BookForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=300)])
    author = StringField('Author', [validators.DataRequired(), personName_, noDigit, validators.Length(min=1, max=30)])
    format = StringField('Format', [validators.DataRequired(), validators.Length(min=1, max=20)])
    pages = IntegerField('Pages', [validators.DataRequired(), number, validators.NumberRange(min=1, max=999999)])
    publisher = StringField('Publisher', [validators.DataRequired(), validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.DataRequired(), noDigit])
    isbn10 = IntegerField('ISBN10', [validators.DataRequired(), number, validators.NumberRange(min=1000000000, max=9999999999)])
    isbn13 = IntegerField('ISBN13', [validators.DataRequired(), number, validators.NumberRange(min=1000000000000, max=9999999999999)])


class MagazineForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=300)])
    publisher = StringField('Publisher', [validators.DataRequired(), validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.DataRequired(), noDigit])
    isbn10 = IntegerField('ISBN10', [validators.DataRequired(), number, validators.NumberRange(min=1000000000, max=9999999999)])
    isbn13 = IntegerField('ISBN13', [validators.DataRequired(), number, validators.NumberRange(min=1000000000000, max=9999999999999)])


class MovieForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=300)])
    director = StringField('Director', [validators.DataRequired(), noDigit,validators.Length(min=1, max=70)])
    producers = StringField('Producers', [validators.DataRequired(), validators.Length(min=1, max=100)])
    actors = StringField('Actors', [validators.DataRequired(), noDigit, validators.Length(min=1, max=300)])
    language = StringField('Language', [validators.DataRequired(), noDigit])
    subtitles = StringField('Subtitles', [validators.DataRequired(), noDigit])
    dubbed = StringField('Dubbed', [noDigit])
    releaseDate = StringField('Release Date', [validators.DataRequired(), date])
    runtime = StringField('Run Time ', [validators.DataRequired(), number, validators.Length(min=1, max=30)])


class MusicForm(Form):
    media_type = StringField('Type', [validators.DataRequired(), validators.Length(min=1, max=5)])
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=300)])
    artist = StringField('Artist', [validators.DataRequired(), validators.Length(min=1, max=70)])
    label = StringField('Label', [validators.DataRequired(), validators.Length(min=1, max=30)])
    releaseDate = StringField('Release Date', [validators.DataRequired(), date, validators.Length(min=1, max=30)])
    asin = StringField('ASIN', [validators.DataRequired(), validators.Length(min=20, max=20)])

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
            form.language.data = item_selected.language
            form.isbn10.data = item_selected.isbn10
            form.isbn13.data = item_selected.isbn13

        elif selected_item_type == 'ma':
            form = MagazineForm(request.form)
            form.title.data = item_selected.title
            form.publisher.data = item_selected.publisher
            form.language.data = item_selected.language
            form.isbn10.data = item_selected.isbn10
            form.isbn13.data = item_selected.isbn13

        elif selected_item_type == 'mo':
            form = MovieForm(request.form)
            form.title.data = item_selected.title
            form.director.data = item_selected.director
            form.producers.data = item_selected.producers
            form.actors.data = item_selected.actors
            form.language.data = item_selected.language
            form.subtitles.data = item_selected.subs
            form.dubbed.data = item_selected.dubbed
            form.releaseDate.data = item_selected.release_date
            form.runtime.data = item_selected.runtime

        elif selected_item_type == 'mu':
            form = MusicForm(request.form)
            form.title.data = item_selected.title
            form.media_type.data = item_selected.media_type
            form.artist.data = item_selected.artist
            form.label.data = item_selected.label
            form.releaseDate.data = item_selected.release_date
            form.asin.data = item_selected.asin

        return form
