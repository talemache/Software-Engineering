import unittest
from unittest import mock
from flask import Flask
from flask_testing import TestCase
from OOZero import create_app
from OOZero.model import db
import OOZero.user_model as user
import OOZero.event_model as event

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
        events = []
        events.append(event.Event(name="Tie my shoe", owner_id=1, event_type=event.EventType.NOTE))
        db.create_all()
        for value in users:
            db.session.add(value)
        for value in events:
            db.session.add(value)
        db.session.commit()

    def tearDown(self):
        """This optional method is called after every test method
        """
        db.drop_all()

    def test_db(self):
        user1 = user.User.query.filter_by(username='test').first()
        event1 = event.Event.query.filter_by(owner_id="1").first()
        self.assertEqual(user1.salt, "saltySalt") #Qurerying database works
        self.assertEqual(event1.name, "Tie my shoe")
        self.assertEqual(event1.owner, user.User.query.filter_by(id='1').first())

    


if __name__ == '__main__':
    unittest.main()