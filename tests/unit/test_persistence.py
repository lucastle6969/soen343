from flask import Flask
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper


app = Flask(__name__)
tdg = Tdg(app)
item_mapper = ItemMapper(tdg)
catalog = item_mapper.get_catalog()


# Tests whether a new book was successfully added, edited, then deleted.
def test_book_persistence(new_book_form):
    item_mapper.add_book(new_book_form)
    item_mapper.end()
    table_name = "book"
    book_id = tdg.get_last_inserted_id(table_name)
    book = catalog.get_item_by_id("bb" + str(book_id))
    assert book is not None

    new_book_form.title.data = "Testing Book"
    item_mapper.find("bb" + str(book_id))
    item_mapper.set_item("bb" + str(book_id), new_book_form)
    item_mapper.end()
    edited_book = catalog.get_item_by_id("bb" + str(book_id))
    assert edited_book.title is "Testing Book"

    item_mapper.delete_item("bb" + str(book_id))
    item_mapper.end()
    removed_book = catalog.get_item_by_id("bb" + str(book_id))
    assert removed_book is None


# Tests whether a new magazine was successfully added, edited, then deleted.
def test_magazine_persistence(new_magazine_form):
    item_mapper.add_magazine(new_magazine_form)
    item_mapper.end()
    table_name = "magazine"
    magazine_id = tdg.get_last_inserted_id(table_name)
    magazine = catalog.get_item_by_id("ma" + str(magazine_id))
    assert magazine is not None

    new_magazine_form.title.data = "Testing Magazine"
    item_mapper.find("ma" + str(magazine_id))
    item_mapper.set_item("ma" + str(magazine_id), new_magazine_form)
    item_mapper.end()
    edited_magazine = catalog.get_item_by_id("ma" + str(magazine_id))
    assert edited_magazine.title is "Testing Magazine"

    item_mapper.delete_item("ma" + str(magazine_id))
    item_mapper.end()
    magazine = catalog.get_item_by_id("ma" + str(magazine_id))
    assert magazine is None


# Tests whether a new movie was successfully added, edited, then deleted.
def test_movie_persistence(new_movie_form):
    item_mapper.add_movie(new_movie_form)
    item_mapper.end()
    table_name = "movie"
    movie_id = tdg.get_last_inserted_id(table_name)
    movie = catalog.get_item_by_id("mo" + str(movie_id))
    assert movie is not None

    new_movie_form.title.data = "Testing Movie"
    item_mapper.find("mo" + str(movie_id))
    item_mapper.set_item("mo" + str(movie_id), new_movie_form)
    item_mapper.end()
    edited_movie = catalog.get_item_by_id("mo" + str(movie_id))
    assert edited_movie.title is "Testing Movie"

    item_mapper.delete_item("mo" + str(movie_id))
    item_mapper.end()
    movie = catalog.get_item_by_id("mo" + str(movie_id))
    assert movie is None


# Tests whether a new music was successfully added, edited, then deleted.
def test_music_persistence(new_music_form):
    item_mapper.add_music(new_music_form)
    item_mapper.end()
    table_name = "music"
    music_id = tdg.get_last_inserted_id(table_name)
    music = catalog.get_item_by_id("mu" + str(music_id))
    assert music is not None

    new_music_form.title.data = "Testing Music"
    item_mapper.find("mu" + str(music_id))
    item_mapper.set_item("mu" + str(music_id), new_music_form)
    item_mapper.end()
    edited_music = catalog.get_item_by_id("mu" + str(music_id))
    assert edited_music.title is "Testing Music"

    item_mapper.delete_item("mu" + str(music_id))
    item_mapper.end()
    music = catalog.get_item_by_id("mu" + str(music_id))
    assert music is None

