import unittest
#from file import class
from Client import Client

#class to test is client information is valid
class ValidateClient(unittest.TestCase):
    
    def validate_client_information(self):
        client = Client(["23452","John","Doe","26 West Village, NY", "johndoe@gmail.com","5142235523","False", "FoundationTrilogy"])
        client.id = "23452"
        client.firstname = "John"
        client.lastname = "Doe"
        client.address = "26, West Village, NY"
        client.email = "johndoe@gmail.com"
        client.phone = "5142235523"
        client.admin = "False"
        client.password = "FoundationTrilogy"
        self.assertEqual(client, client) #Check for expected value

