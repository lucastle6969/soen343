from flask import Flask
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper


app = Flask(__name__)
tdg = Tdg(app)
item_mapper = ItemMapper(tdg)
catalog = item_mapper.get_catalog()


# Tests whether a new book was successfully added to the working memory
def test_add_book_working_memory(new_book):
    catalog.add_item(new_book)
    book = catalog.get_item_by_id(new_book.prefix + str(new_book.id))
    assert book is not None
    catalog.delete_last_item()


# Tests whether a new magazine was successfully added to the working memory
def test_add_magazine_working_memory(new_magazine):
    catalog.add_item(new_magazine)
    magazine = catalog.get_item_by_id(new_magazine.prefix + str(new_magazine.id))
    assert magazine is not None
    catalog.delete_last_item()


# Tests whether a new movie was successfully added to the working memory
def test_add_movie_working_memory(new_movie):
    catalog.add_item(new_movie)
    movie = catalog.get_item_by_id(new_movie.prefix + str(new_movie.id))
    assert movie is not None
    catalog.delete_last_item()


# Tests whether a new music was successfully added to the working memory
def test_add_music_working_memory(new_music):
    catalog.add_item(new_music)
    music = catalog.get_item_by_id(new_music.prefix + str(new_music.id))
    assert music is not None
    catalog.delete_last_item()


# Tests whether a new book was successfully added to the database
def test_add_book_persistence(new_book_form):
    item_mapper.add_book(new_book_form)
    item_mapper.end()
    table_name = "book"
    book_id = tdg.get_last_inserted_id(table_name)
    book = catalog.get_item_by_id("bb" + str(book_id))
    assert book is not None


# Tests whether a new magazine was successfully added to the database
def test_add_magazine_persistence(new_magazine_form):
    item_mapper.add_magazine(new_magazine_form)
    item_mapper.end()
    table_name = "magazine"
    magazine_id = tdg.get_last_inserted_id(table_name)
    magazine = catalog.get_item_by_id("ma" + str(magazine_id))
    assert magazine is not None


# Tests whether a new movie was successfully added to the database
def test_add_movie_persistence(new_movie_form):
    item_mapper.add_movie(new_movie_form)
    item_mapper.end()
    table_name = "movie"
    movie_id = tdg.get_last_inserted_id(table_name)
    movie = catalog.get_item_by_id("mo" + str(movie_id))
    assert movie is not None


# Tests whether a new music was successfully added to the database
def test_add_music_persistence(new_music_form):
    item_mapper.add_music(new_music_form)
    item_mapper.end()
    table_name = "music"
    music_id = tdg.get_last_inserted_id(table_name)
    music = catalog.get_item_by_id("mu" + str(music_id))
    assert music is not None
