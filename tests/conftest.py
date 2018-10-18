# file contains fixtures/setup functions used for all test files.

import pytest

from model.User import Client
from model.User import Admin
from model.Item import Book, Magazine, Movie, Music

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