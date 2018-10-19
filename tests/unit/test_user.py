#from file import class
from model.User import User


#Note: Functions need to start with test_
def test_new_user(new_user):
    assert new_user.id == '23452'
    assert new_user.firstname == 'John'
    assert new_user.lastname == 'Doe'
    assert new_user.address == 'Sunset Avenue'
    assert new_user.email == 'johndoe@gmail.com'
    assert new_user.phone == '5142235523'
    assert new_user.admin == 0
    assert new_user.password == 'FoundationSeries'

