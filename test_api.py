from twisted.trial import unittest
from twisted.internet import reactor, defer
import txmongo
import os
import bcrypt
from datetime import date 
from api import Api, UserAlreadyExists


DB_PORT = int(os.environ["DB_PORT"])

class ApiTest(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.conn = yield txmongo.MongoConnection('127.0.0.1', DB_PORT)
        self.db = self.conn.test_db
        self.api = Api(self.db, bcrypt.gensalt())

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.db.user.drop()
        yield self.db.firm.drop()
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_user_create(self):
        name = "user"
        fullname = "User User"
        password = "password"
        yield self.api.create_user(name, fullname, password)
        [user] = yield self.api.get_user(name)
        self.assertEqual(user['name'], "user")
        self.assertEqual(user['fullname'], "User User")
        self.assertEqual(user['password'], self.api.hash_password("password".encode('utf-8')))

    @defer.inlineCallbacks
    def test_user_already_exists(self):
        name = "user"
        fullname = "User User"
        password = "password"
        yield self.api.create_user(name, fullname, password)
        yield self.assertFailure(self.api.create_user(name, fullname, password), UserAlreadyExists)

    @defer.inlineCallbacks
    def test_create_firms(self):
        name= 'My firm' 
        adress = 'Riksdalersgatan 25C'
        postal_code = '41481'
        city = 'Gothenburg'
        yield self.api.create_firm(name, adress, postal_code, city)

        adress2 = 'Marklandsgatan 67'
        postal_code2 = '1234'

        yield self.api.create_firm(name, adress2, postal_code2, city)

        [firm1, firm2] = yield self.api.get_firms({'name': name})

        self.assertEqual(firm1['name'], name)
        self.assertEqual(firm1['adress'], adress)
        self.assertEqual(firm1['postal_code'],postal_code)
        self.assertEqual(firm1['city'],city)

        self.assertEqual(firm2['adress'],adress2)

        [firm] = yield self.api.get_firms({'adress':adress2})
        self.assertEqual(firm['adress'],adress2)
