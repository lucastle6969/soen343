# file contains fixtures/setup functions used for all test files.

import pytest

from model.User import User
from model.Item import Book, Magazine, Movie, Music
from model.Form import BookForm, MagazineForm, MovieForm, MusicForm


# user created to be used for testing that are in the module scope
@pytest.fixture(scope='module')
def new_user():
    user = User('23452', 'John', 'Doe', 'Sunset Avenue', 'johndoe@gmail.com', '5142235523', 0, 'FoundationSeries')
    return user


# Book created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_book():
    book = Book(324, "DARK MATTER", "bb", "Blake Crouch", "Hardcover", 300, "VonRueden-Swaniawski", 2015, "EN", 5914602904, 5914602904123, 1, 1)
    return book


# Magazine created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_magazine():
    magazine = Magazine(333, "The UFO Incident", "ma", "Kuhic Ferry", "Nov. 23 2014", "EN", 7464072294, 7464072294123, 1, 2)
    return magazine


# Movie created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_movie():
    movie = Movie(434, "Man Is Not a Bird", "mo", "Gorden Kermon", "Skiles Swaniawski", "Eleen Leavesley", "EN", "None", "None", "18/10/2018", "2h30", 1, 3)
    return movie


# Music created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_music():
    music = Music(331, "Boiling Point", "mu", "CD", "Dianna Argo", "Sony Music", "19/01/1976", "B008FOB124", 1, 4)
    return music


# Book form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_book_form():
    form = BookForm()
    form.title.data = "DARK MATTER"
    form.author.data = "Blake Crouch"
    form.format.data = "Hardcover"
    form.pages.data = 300
    form.publisher.data = "VonRueden-Swaniawski"
    form.publication_year.data = 2015
    form.language.data = "EN"
    form.isbn10.data = 5914602904
    form.isbn13.data = 5914602904123
    form.quantity.data = 3
    return form


# Magazine form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_magazine_form():
    form = MagazineForm()
    form.title.data = "The UFO Incident"
    form.publisher.data = "Kuhic Ferry"
    form.publication_date.data = "Nov. 23 2014"
    form.language.data = "EN"
    form.isbn10.data = 7464072294
    form.isbn13.data = 7464072294123
    form.quantity.data = 1
    return form


# Movie form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_movie_form():
    form = MovieForm()
    form.title.data = "Man Is Not a Bird"
    form.director.data = "Gorden Kermon"
    form.producers.data = "Skiles Swaniawski"
    form.actors.data = "Eleen Leavesley"
    form.language.data = "EN"
    form.subtitles.data = "None"
    form.dubbed.data = "None"
    form.release_date.data = "18/10/2018"
    form.runtime.data = "2h30"
    form.quantity.data = 1
    return form


# Music form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_music_form():
    form = MusicForm()
    form.title.data = "Man Is Not a Bird"
    form.media_type.data = "CD"
    form.artist.data = "Dianna Argo"
    form.label.data = "Sony Music"
    form.release_date.data = "19/01/1976"
    form.asin.data = "B008FOB124"
    form.quantity.data = 1
    return form


