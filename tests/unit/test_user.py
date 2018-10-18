#from file import class
from model.User import Client
from model.User import Admin

#Note: Functions need to start with test_
def test_new_user(new_client):
    assert new_client.id == '23452'
    assert new_client.firstname == 'John'
    assert new_client.lastname == 'Doe'
    assert new_client.address == 'Sunset Avenue'
    assert new_client.email == 'johndoe@gmail.com'
    assert new_client.phone == '5142235523'
    assert new_client.admin == 0
    assert new_client.password == 'FoundationSeries'

def test_new_admin(new_admin):
    assert new_admin.id == '235'
    assert new_admin.firstname == 'Jane'
    assert new_admin.lastname == 'Doe'
    assert new_admin.address == 'End of Eternity'
    assert new_admin.email == 'janedoe@gmail.com'
    assert new_admin.phone == '51422643634'
    assert new_admin.admin == 1
    assert new_admin.password == 'isaacAsimov'