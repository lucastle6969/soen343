from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt

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
    def getFormForItemType(type, form):
        if type == 'bb':
            return BookForm(form)
        elif type == 'ma':
            return MagazineForm(form)
        elif type == 'mo':
            return MovieForm(form)
        elif type == "mu":
            return MusicForm(form)
        else:
            return None

    @staticmethod
    def getFormData(itemSelected, request):
        seletedItemType = itemSelected.prefix
        form = None
        if seletedItemType == 'bb':
            form = BookForm(request.form)
            form.title.data = itemSelected.title
            form.author.data = itemSelected.author
            form.format.data = itemSelected.format
            form.pages.data = itemSelected.pages
            form.publisher.data = itemSelected.publisher
            form.language.data = itemSelected.language
            form.isbn10.data = itemSelected.isbn10
            form.isbn13.data = itemSelected.isbn13

        elif seletedItemType == 'ma':
            form = MagazineForm(request.form)
            form.title.data = itemSelected.title
            form.publisher.data = itemSelected.publisher
            form.language.data = itemSelected.language
            form.isbn10.data = itemSelected.isbn10
            form.isbn13.data = itemSelected.isbn13

        elif seletedItemType == 'mo':
            form = MovieForm(request.form)
            form.title.data = itemSelected.title
            form.director.data = itemSelected.director
            form.producers.data = itemSelected.producers
            form.actors.data = itemSelected.actors
            form.language.data = itemSelected.language
            form.subtitles.data = itemSelected.subs
            form.dubbed.data = itemSelected.dubbed
            form.releaseDate.data = itemSelected.release_date
            form.runtime.data = itemSelected.runtime

        elif seletedItemType == 'mu':
            form = MusicForm(request.form)
            form.title.data = itemSelected.title
            form.media_type.data = itemSelected.media_type
            form.artist.data = itemSelected.artist
            form.label.data = itemSelected.label
            form.releaseDate.data = itemSelected.release_date
            form.asin.data = itemSelected.asin

        return form