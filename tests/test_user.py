import unittest
from unittest import mock
from flask import Flask
from flask_testing import TestCase
from OOZero import create_app
from OOZero.model import db
import OOZero.user_model as user

class TestUser(TestCase):

    def create_app(self):
        app = create_app("OOZero.config.TestingConfig")
        return app

    def setUpClass():
        """This optional method is called once for this test class
        """
        pass

    def tearDownClass():
        """This optional method is called once for this test class
        """
        pass

    def setUp(self):
        """This optional method is called before every test method
        """
        db.create_all()
        db.session.add(user.User(username="username", name="name", email="email@email.email", password_hash="password_hash", salt="salt", profile_picture=b"profile_picture"))
        db.session.add(user.User(username="test", password_hash="iiojfeaioieof", salt="saltySalt"))
        db.session.commit()

    def tearDown(self):
        """This optional method is called after every test method
        """
        db.session.remove()
        db.drop_all()

    def test_db(self):
        user1 = user.User.query.filter_by(username='test').first()
        self.assertEqual(user1.salt, "saltySalt")

    def test_getUser(self):
        pass

    def test_addUser(self):
        pass

    def test_removeUser(self):
        pass

    def test_authenticateUser(self):
        pass


if __name__ == '__main__':
    unittest.main()