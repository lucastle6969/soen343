# file contains fixtures/setup functions used for all test files.

#import os
#import tempfile
#import pytest

#from flaskext.mysql import MySQL
#from model import Tdg
#from model import User

#pytest_plugins = ['pytest_virtualenv']

#@pytest.fixture(scope='module')
#def new_user_creation():
#    user = User('4134','john', 'doe', 'Sunset Avenue', 'johnDoe@gmail.com','5142234443',0,'FairytaleGoneBad')
#    return user

#@pytest.fixture(scope='session')


import pytest
from model.User import Client
from model.User import Admin

#user created to be used for testing that are in the module scope
@pytest.fixture(scope='module')
def new_client():
    client = Client('23452','John','Doe','Sunset Avenue', 'johndoe@gmail.com','5142235523', 0, 'FoundationSeries')
    return client

#user created to be used for testing that are in the module scope
@pytest.fixture(scope='module')
def new_admin():
    admin = Admin('235','Jane','Doe','End of Eternity', 'janedoe@gmail.com','51422643634', 1, 'isaacAsimov')
    return admin



