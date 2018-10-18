# file contains fixtures/setup functions used for all test files.

import pytest

from wtforms import Form
from model.User import Client
from model.User import Admin
from model.Item import Book, Magazine, Movie, Music
from model.Form import RegisterForm, BookForm, MagazineForm, MovieForm, MusicForm, Forms

# user created to be used for testing that are in the module scope
@pytest.fixture(scope='module')
def new_client():
    client = Client('23452','John','Doe','Sunset Avenue', 'johndoe@gmail.com','5142235523', 0, 'FoundationSeries')
    return client

# user created to be used for testing that are in the module scope
@pytest.fixture(scope='module')
def new_admin():
    admin = Admin('235','Jane','Doe','End of Eternity', 'janedoe@gmail.com','51422643634', 1, 'isaacAsimov')
    return admin

# Book created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_book():
    book = Book("DARK MATTER", "bb", 324, "avail", "Blake Crouch", "Hardcover", "300", "EN", "VonRueden-Swaniawski", 5914602904, "5914602904123")
    return book

# Magazine created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_magazine():
    magazine = Magazine("The UFO Incident", "ma", 333, "avail", "Kuhic Ferry", "EN", 7464072294, 7464072294123)
    return magazine

# Movie created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_movie():
    movie = Movie("Man Is Not a Bird", "mo", 434, "avail", "Gorden Kermon", "Skiles Swaniawski", "Eleen Leavesley", "EN", "None", "None", "18/10/2018", "2h30")
    return movie

# Music created for testing insertion, deletion and modification
@pytest.fixture(scope='module')
def new_music():
    music = Music("Boiling Point", "mu", 331, "avail", "CD", "Dianna Argo", "19/01/1976", "B008FOB124")
    return music

# Book form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_book_form():
    form = BookForm()
    form.title.data = "DARK MATTER"
    form.author.data = "bb"
    form.format.data = "Hardcover"
    form.pages.data = 300
    form.publisher.data = "VonRueden-Swaniawski"
    form.language.data = "EN"
    form.isbn13.data = 5914602904
    form.isbn13.data = 5914602904123
    return form

# Magazine form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_magazine_form():
    form = MagazineForm()
    form.title.data = "The UFO Incident"
    form.publisher.data = "Kuhic Ferry"
    form.language.data = "EN"
    form.isbn13.data = 7464072294
    form.isbn13.data = 7464072294123
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
    form.releaseDate.data = "18/10/2018"
    form.runtime.data = "2h30"
    return form

# Music form represents form sent with POST request from front-end
@pytest.fixture(scope='module')
def new_music_form():
    form = MusicForm()
    form.title.data = "Man Is Not a Bird"
    form.media_type.data = "CD"
    form.artist.data = "Dianna Argo"
    form.label.data = "Eleen Leavesley"
    form.releaseDate.data = "19/01/1976"
    form.asin.data = "B008FOB124"
    return form
