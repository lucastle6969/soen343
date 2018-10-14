from wtforms import Form, StringField, PasswordField, validators, IntegerField


class RegisterForm(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=50)])
    lastname = StringField('Last Name', [validators.Length(min=1, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    phone = StringField('Phone', [validators.Length(min=1, max=12)])
    address = StringField('Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirmed Password')


class BookForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    author = StringField('Author', [validators.Length(min=1, max=30)])
    format = StringField('Format', [validators.Length(min=1, max=20)])
    pages = IntegerField('Pages', [validators.NumberRange(min=1, max=999999)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    isbn10 = IntegerField('ISBN10', [validators.NumberRange(min=1000000000, max=9999999999)])
    isbn13 = IntegerField('ISBN13', [validators.NumberRange(min=1000000000000, max=9999999999999)])


class MagazineForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    isbn10 = IntegerField('ISBN10', [validators.NumberRange(min=1000000000, max=9999999999)])
    isbn13 = IntegerField('ISBN13', [validators.NumberRange(min=1000000000000, max=9999999999999)])


class MovieForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    director = StringField('Director', [validators.Length(min=1, max=30)])
    producers = StringField('Producers', [validators.Length(min=1, max=100)])
    actors = StringField('Actors', [validators.Length(min=1, max=100)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    subtitles = StringField('Subtitles', [validators.Length(min=1, max=30)])
    dubbed = StringField('Dubbed', [validators.Length(min=1, max=30)])
    releaseDate = StringField('Release Date', [validators.Length(min=1, max=30)])
    runtime = StringField('Run Time ', [validators.Length(min=1, max=30)])


class MusicForm(Form):
    media_type = StringField('Type', [validators.Length(min=1, max=10)])
    title = StringField('Title', [validators.Length(min=1, max=100)])
    artist = StringField('Artist', [validators.Length(min=1, max=30)])
    label = StringField('Label', [validators.Length(min=1, max=30)])
    releaseDate = StringField('Release Date', [validators.Length(min=1, max=30)])
    asin = StringField('ASIN', [validators.Length(min=1, max=20)])


class ItemForm(Form):
   
    # The following only applies to Book items
    title = StringField('Title', [validators.Length(min=1, max=100)])
    author = StringField('Author', [validators.Length(min=1, max=30)])
    format = StringField('Format', [validators.Length(min=1, max=20)])
    pages = IntegerField('Number of pages', [validators.Length(min=1, max=20)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    isbn10 = IntegerField('ISBN-10', [validators.Length(min=1, max=10)])
    isbn13 = IntegerField('ISBN-13', [validators.Length(min=1, max=10)])


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
