from flask import Flask
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper


app = Flask(__name__)
tdg = Tdg(app)
item_mapper = ItemMapper(tdg)
catalog = item_mapper.get_catalog()


# Tests whether a new book was successfully removed from the working memory
def test_remove_book_working_memory(new_book):
    catalog.add_item(new_book)
    catalog.delete_items([new_book])
    book = catalog.get_item_by_id(new_book.prefix, new_book.id)
    assert book is None


# Tests whether a new magazine was successfully removed from the working memory
def test_remove_magazine_working_memory(new_magazine):
    catalog.add_item(new_magazine)
    catalog.delete_items([new_magazine])
    magazine = catalog.get_item_by_id(new_magazine.prefix, new_magazine.id)
    assert magazine is None


# Tests whether a new movie was successfully removed from the working memory
def test_remove_movie_working_memory(new_movie):
    catalog.add_item(new_movie)
    catalog.delete_items([new_movie])
    movie = catalog.get_item_by_id(new_movie.prefix, new_movie.id)
    assert movie is None


# Tests whether a new music was successfully removed from the working memory
def test_remove_music_working_memory(new_music):
    catalog.add_item(new_music)
    catalog.delete_items([new_music])
    music = catalog.get_item_by_id(new_music.prefix, new_music.id)
    assert music is None
