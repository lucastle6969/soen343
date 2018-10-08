from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

class RegisterForm(Form):
    type = StringField('Type', [validators.Length(min=1, max=10)])
    title = StringField('Title', [validators.Length(min=1, max=100)])
    artist = StringField('Artist', [validators.Length(min=1, max=30)])
    label = StringField('Label', [validators.Length(min=1, max=30)])
    releaseDate = StringField('Release Date', [validators.Length(min=1, max=30)])
    asin = StringField('ASIN', [validators.Length(min=1, max=20)])