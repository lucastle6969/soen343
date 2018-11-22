from flask import Flask
from model.Tdg import Tdg
from model.ItemMapper import ItemMapper
import pytest

app = Flask(__name__)
tdg = Tdg(app)
item_mapper = ItemMapper(app)
catalog = item_mapper.get_catalog()


@pytest.fixture(scope='function')
def get_last_inserted_id(tdg_, table_name):
    connection = tdg_.mysql.connect()
    cur = connection.cursor()

    result = cur.execute("SELECT * FROM " + table_name + " ORDER BY id DESC LIMIT 1")
    item_id = cur.fetchone()
    cur.close()

    if result > 0:
        return item_id[0]
    else:
        item_id = False
    return item_id


@pytest.fixture(scope='function')
def del_physical(tdg_, table_name, attr_name, item_id):
    connection = tdg_.mysql.connect()
    cur = connection.cursor()

    cur.execute("DELETE FROM " + table_name + " WHERE " + attr_name + " = " + item_id)
    cur.close()


# Tests whether a new book was successfully added, edited, then deleted.
def test_book_persistence(new_book_form):
    item_mapper.add_book(new_book_form)
    item_mapper.end()
    table_name = "book"
    book_id = get_last_inserted_id(tdg, table_name)
    book = catalog.get_item_by_id("bb", book_id)
    assert book is not None

    new_book_form.title.data = "Testing Book"
    item_mapper.find("bb", book_id)
    item_mapper.set_item("bb", book_id, new_book_form, 0, None)
    item_mapper.end()
    edited_book = catalog.get_item_by_id("bb", book_id)
    assert edited_book.title is "Testing Book"

    item_mapper.delete_item("bb", book_id)
    item_mapper.end()
    removed_book = catalog.get_item_by_id("bb", book_id)
    assert removed_book is None

    del_physical(tdg, 'book_physical', 'item_fk', str(book_id))
    keys = tdg.get_physical_keys(book_id, "bb")
    assert len(keys) == 0


# Tests whether a new magazine was successfully added, edited, then deleted.
def test_magazine_persistence(new_magazine_form):
    item_mapper.add_magazine(new_magazine_form)
    item_mapper.end()
    table_name = "magazine"
    magazine_id = get_last_inserted_id(tdg, table_name)
    magazine = catalog.get_item_by_id("ma", magazine_id)
    assert magazine is not None

    new_magazine_form.title.data = "Testing Magazine"
    item_mapper.find("ma", magazine_id)
    item_mapper.set_item("ma", magazine_id, new_magazine_form, 0, None)
    item_mapper.end()
    edited_magazine = catalog.get_item_by_id("ma", magazine_id)
    assert edited_magazine.title is "Testing Magazine"

    item_mapper.delete_item("ma", magazine_id)
    item_mapper.end()
    magazine = catalog.get_item_by_id("ma", magazine_id)
    assert magazine is None

    del_physical(tdg, 'magazine_physical', 'item_fk', str(magazine_id))
    keys = tdg.get_physical_keys(magazine_id, "ma")
    assert len(keys) == 0


# Tests whether a new movie was successfully added, edited, then deleted.
def test_movie_persistence(new_movie_form):
    item_mapper.add_movie(new_movie_form)
    item_mapper.end()
    table_name = "movie"
    movie_id = get_last_inserted_id(tdg, table_name)
    movie = catalog.get_item_by_id("mo", movie_id)
    assert movie is not None

    new_movie_form.title.data = "Testing Movie"
    item_mapper.find("mo", movie_id)
    item_mapper.set_item("mo", movie_id, new_movie_form, 0, None)
    item_mapper.end()
    edited_movie = catalog.get_item_by_id("mo", movie_id)
    assert edited_movie.title is "Testing Movie"

    item_mapper.delete_item("mo", movie_id)
    item_mapper.end()
    movie = catalog.get_item_by_id("mo", movie_id)
    assert movie is None

    del_physical(tdg, 'movie_physical', 'item_fk', str(movie_id))
    keys = tdg.get_physical_keys(movie_id, "mo")
    assert len(keys) == 0


# Tests whether a new music was successfully added, edited, then deleted.
def test_music_persistence(new_music_form):
    item_mapper.add_music(new_music_form)
    item_mapper.end()
    table_name = "music"
    music_id = get_last_inserted_id(tdg, table_name)
    music = catalog.get_item_by_id("mu", music_id)
    assert music is not None

    new_music_form.title.data = "Testing Music"
    item_mapper.find("mu", music_id)
    item_mapper.set_item("mu", music_id, new_music_form, 0, None)
    item_mapper.end()
    edited_music = catalog.get_item_by_id("mu", music_id)
    assert edited_music.title is "Testing Music"

    item_mapper.delete_item("mu", music_id)
    item_mapper.end()
    music = catalog.get_item_by_id("mu", music_id)
    assert music is None

    del_physical(tdg, 'music_physical', 'item_fk', str(music_id))
    keys = tdg.get_physical_keys(music_id, "mu")
    assert len(keys) == 0
