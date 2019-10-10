import unittest
from unittest import mock
from flask import Flask
from flask_testing import TestCase
from OOZero import create_app
from OOZero.model import db
import OOZero.user_model as user

class TestUser(TestCase, unittest.TestCase):

    def create_app(self):
        app = create_app("OOZero.config.TestingConfig")
        return app

    @classmethod
    def setUpClass(cls):
        """This optional method is called once for this test class
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """This optional method is called once for this test class
        """
        pass

    def setUp(self):
        """This optional method is called before every test method
        """
        users = []
        users.append(user.User(username="username", name="name", email="email@email.email", password_hash="password_hash", salt="salt", profile_picture=b"profile_picture"))
        users.append(user.User(username="test", password_hash="iiojfeaioieof", salt="saltySalt"))
        users.append(user.User(username="jeff", name="jeff bob", password_hash="eeeeeeeeeeeeeee", salt="fffffffffffffff"))
        users.append(user.User(username="epicUsername69", email="aaaa@gmail.com", password_hash="asdfafeadf", salt="graefgafae"))
        db.create_all()
        for value in users:
            db.session.add(value)
        db.session.commit()

    def tearDown(self):
        """This optional method is called after every test method
        """
        #db.session.remove()
        db.drop_all()

    def test_db(self):
        user1 = user.User.query.filter_by(username='test').first()
        self.assertEqual(user1.salt, "saltySalt") #Qurerying database works

    def test_getUser(self):
        person = user.getUser("username")
        self.assertEqual(person.salt, "salt") #Retreive by username works
        testPerson = user.User.query.filter_by(username="jeff").first()
        person = user.getUser(testPerson.id)
        self.assertEqual(person.name, "jeff bob") #Retreive by id works
        self.assertRaises(TypeError, lambda : user.getUser(user.User())) #Does not accept User objects
        self.assertRaises(TypeError, lambda : user.getUser(3.4)) #Does not accept floats

    def test_addUser(self):
        pass

    def test_removeUser(self):
        pass

    def test_authenticateUser(self):
        pass


if __name__ == '__main__':
    unittest.main()