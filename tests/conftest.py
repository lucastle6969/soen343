# file contains fixtures/setup functions used for all test files.

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



