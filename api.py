import txmongo
import os
from twisted.internet import defer
import bcrypt
import sys


class Api():

    def __init__(self, db, salt):
        self.db = db
        self.salt = salt

    def hash_password(self, password):
        return bcrypt.hashpw(password, self.salt)

    @defer.inlineCallbacks
    def create_user(self, name, fullname, password):
        users = yield self.get_user(name)
        if users != []:
            raise UserAlreadyExists("username %s is not unique".format(name))

        hashed = self.hash_password(password.encode('utf-8'))
        
        yield self.db.user.insert({
            'name': name,
            'fullname': fullname,
            'password': hashed
        })

    @defer.inlineCallbacks
    def get_user(self, name):
        user = yield self.db.user.find({'name':name}, limit=1)
        return user


    @defer.inlineCallbacks
    def create_firm(self, name, adress, postal_code, city):
        yield self.db.firm.insert({
            'name': name,
            'adress': adress,
            'postal_code': postal_code,
            'city': city
        })

    @defer.inlineCallbacks
    def get_firms(self, selectors):
        firms = yield self.db.firm.find(selectors)
        return firms
        

class UserAlreadyExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 


