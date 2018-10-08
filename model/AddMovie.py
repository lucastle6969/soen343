from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

class MovieForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    director = StringField('Director', [validators.Length(min=1, max=30)])
    producers = StringField('Producers', [validators.Length(min=1, max=100)])
    actors = StringField('Actors', [validators.Length(min=1, max=100)])
    language = StringField('Language', [validators.Length(min=1, max=30)])
    subtitles = StringField('Subtitles', [validators.Length(min=1, max=30)])
    dubbed = StringField('Dubbed', [validators.Length(min=1, max=30)])
    releaseDate = StringField('Release Date', [validators.Length(min=1, max=30)])
    runTime = StringField('Run Time ', [validators.Length(min=1, max=30)])