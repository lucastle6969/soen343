from flask import Flask
from model.ItemMapper import ItemMapper


app = Flask(__name__)
item_mapper = ItemMapper(app)
catalog = item_mapper.get_catalog()


# Tests whether a new book was successfully added to the working memory
def test_add_book_working_memory(new_book):
    catalog.add_item(new_book)
    book = catalog.get_item_by_id(new_book.prefix, new_book.id)
    assert book is not None
    catalog.delete_last_item()


# Tests whether a new magazine was successfully added to the working memory
def test_add_magazine_working_memory(new_magazine):
    catalog.add_item(new_magazine)
    magazine = catalog.get_item_by_id(new_magazine.prefix, new_magazine.id)
    assert magazine is not None
    catalog.delete_last_item()


# Tests whether a new movie was successfully added to the working memory
def test_add_movie_working_memory(new_movie):
    catalog.add_item(new_movie)
    movie = catalog.get_item_by_id(new_movie.prefix, new_movie.id)
    assert movie is not None
    catalog.delete_last_item()


# Tests whether a new music was successfully added to the working memory
def test_add_music_working_memory(new_music):
    catalog.add_item(new_music)
    music = catalog.get_item_by_id(new_music.prefix, new_music.id)
    assert music is not None
    catalog.delete_last_item()
