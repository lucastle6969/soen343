from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

class BookForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    author = StringField('Author', [validators.Length(min=1, max=30)])
    format = StringField('Format', [validators.Length(min=1, max=20)])
    pages = IntegerField('Pages', [validators.NumberRange(min=1, max=255)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    isbn10 = IntegerField('ISBN10', [validators.NumberRange(min=1, max=10)])
    isbn13 = IntegerField('ISBN13', [validators.NumberRange(min=1, max=13)])