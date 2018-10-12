from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, validators

class ItemForm(Form):
    # Todo: Create a different validators for the different type of items
    # The following only applies to Book items
    title = StringField('Title', [validators.Length(min=1, max=100)])
    author = StringField('Author', [validators.Length(min=1, max=30)])
    format = StringField('Format', [validators.Length(min=1, max=20)])
    pages = IntegerField('Number of pages', [validators.Length(min=1, max=20)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    isbn10 = IntegerField('ISBN-10', [validators.Length(min=1, max=10)])
    isbn13 = IntegerField('ISBN-13', [validators.Length(min=1, max=10)])