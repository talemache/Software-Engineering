import unittest
from unittest import mock
from flask import Flask
from flask_testing import TestCase
from OOZero import create_app
from OOZero.model import db
import OOZero.user_model as user
import OOZero.event_model as event
import datetime

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
        events.append(event.Event(name="Raid Area 51", owner_id=1, parent_id=1, event_type=event.EventType.NOTE))
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
        self.assertTrue(event1 in user.User.query.filter_by(id='1').first().events)

    def test_parent(self):
        event0 = event.Event.query.filter_by(id="1").first()
        event1 = event.Event.query.filter_by(id="2").first()
        self.assertIsNotNone(event0)
        self.assertIsNotNone(event1)
        self.assertEqual(event0, event1.parent)
        #self.assertTrue(event1 in event0.children)

    def test_createEventValues(self):
        event0 = event.createEvent("cool hat", 1, event.EventType.NOTE)
        self.assertEqual(event0.name, "cool hat")
        event1 = event.createEvent("cooler hat", 1, event.EventType.REMINDER, discrption="A very cool hat", start_time=datetime.datetime.utcnow())
        self.assertEqual(event1.discrption, "A very cool hat")
        event2 = event.createEvent("Best hat", 1, event.EventType.NOTE, parent=1)
        self.assertEqual(event2.parent, event.Event.query.filter_by(id=1).first())

    def test_createEventRanges(self):
        self.assertRaises(ValueError, lambda: event.createEvent(None, 1, event.EventType.NOTE))
        self.assertRaises(ValueError, lambda: event.createEvent("1" * 61, 1, event.EventType.NOTE))
        self.assertRaises(ValueError, lambda: event.createEvent("hi", None, event.EventType.NOTE))
        self.assertRaises(ValueError, lambda: event.createEvent("hi", 1, 12))
        self.assertRaises(ValueError, lambda: event.createEvent("hi", 1, event.EventType.NOTE, parent=50))

    def test_createEventTypes(self):
        event0 = event.createEvent("cool hat", 1, event.EventType.NOTE)
        self.assertEqual(event0.name, "cool hat")
        self.assertRaises(ValueError, lambda: event.createEvent("hi", 1, event.EventType.NOTE, start_time=datetime.datetime.utcnow()))
        event0 = event.createEvent("This is a thing", 1, event.EventType.ENCRYPTED, discrption="Hidden text", password="mushSecure")
        self.assertNotEqual(event0.discrption, "Hidden text")
        self.assertEqual(event.decrypt(event0.discrption, "mushSecure"), "Hidden text")
        self.assertRaises(TypeError, lambda: event.createEvent("encrypted", 1, event.EventType.ENCRYPTED))
        event0 = event.createEvent("event", 1, event.EventType.EVENT, start_time=datetime.datetime.utcnow(), end_time=datetime.datetime.utcnow())
        self.assertEqual(event0.name, "event")
        self.assertRaises(ValueError, lambda: event.createEvent("event", 1, event.EventType.EVENT, start_time=datetime.datetime.utcnow()))
        self.assertRaises(ValueError, lambda: event.createEvent("event", 1, event.EventType.EVENT, end_time=datetime.datetime.utcnow()))
        self.assertRaises(ValueError, lambda: event.createEvent("event", 1, event.EventType.EVENT))
        event0 = event.createEvent("REMINDER", 1, event.EventType.REMINDER, start_time=datetime.datetime.utcnow())
        self.assertEqual(event0.name, "REMINDER")
        self.assertRaises(ValueError, lambda: event.createEvent("REMINDER", 1, event.EventType.REMINDER, start_time=datetime.datetime.utcnow(), end_time=datetime.datetime.utcnow()))
        self.assertRaises(ValueError, lambda: event.createEvent("REMINDER", 1, event.EventType.REMINDER, end_time=datetime.datetime.utcnow()))
        self.assertRaises(ValueError, lambda: event.createEvent("REMINDER", 1, event.EventType.REMINDER))

    def test_generateKey(self):
        self.assertEqual(event.generateKey("help"), b'F4LKJgsRbCNgghB4h152bgO6HNtUc4FBbi-r4cSVgEs=')
        self.assertEqual(event.generateKey("this could be a password"), event.generateKey("this could be a password"))

    def test_encrypt(self):
        ciphertext = event.encrypt("some secret thing", "some password")
        self.assertNotEqual(ciphertext, "some secret thing")

    def test_decrypt(self):
        ciphertext = event.encrypt("some secret thing", "some password")
        self.assertEqual(event.decrypt(ciphertext, "some password"), "some secret thing")
        self.assertIsNone(event.decrypt(ciphertext, "wrong password"))

if __name__ == '__main__':
    unittest.main()