#from file import class
from model.User import User

#Note: Functions need to start with test_
def test_new_user():
    user = User('23452','John','Doe','Sunset Avenue', 'johndoe@gmail.com','5142235523', 0, 'FoundationTrilogy')
    user.id = '23452'
    user.firstname = 'John'
    user.lastname = 'Doe'
    user.address = 'Sunset Avenue'
    user.email = 'johndoe@gmail.com'
    user.phone = '5142235523'
    user.admin = 0
    user.password = 'FoundationTrilogy'
    assert(user == user) #Check for expected value

