from flask import Flask, render_template, flash, redirect, url_for, session, request
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper

app = Flask(__name__)
tdg = Tdg(app)
item_mapper = ItemMapper(tdg)

# Tests whether a new book was successfully added to the working memory
def test_add_book_working_memory(new_book_form):
    result = item_mapper.add_book(new_book_form)
    assert result


# Tests whether a new magazine was successfully added to the working memory
def test_add_magazine_working_memory(new_magazine_form):
    result = item_mapper.add_magazine(new_magazine_form)
    assert result


# Tests whether a new movie was successfully added to the working memory
def test_add_movie_working_memory(new_movie_form):
    result = item_mapper.add_movie(new_movie_form)
    assert result


# Tests whether a new music was successfully added to the working memory
def test_add_music_working_memory(new_music_form):
    result = item_mapper.add_music(new_music_form)
    assert result
