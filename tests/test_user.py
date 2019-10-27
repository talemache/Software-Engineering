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
        newUser = user.addUser("dust", "goodPassword") 
        self.assertEqual(newUser, user.getUser("dust")) #Add user
        self.assertRaises(ValueError, lambda: user.addUser("", "goodPassword")) #Min length username
        self.assertRaises(ValueError, lambda: user.addUser("f" * 31, "goodPassword")) #Max length username
        self.assertRaises(TypeError, lambda: user.addUser(None, "goodPassword")) #Username type
        self.assertRaises(ValueError, lambda: user.addUser("another", "123")) #Min length password
        self.assertRaises(TypeError, lambda: user.addUser("one", None)) #Password type
        self.assertRaises(ValueError, lambda: user.addUser("bytes", "goodPassword", name="F" * 61)) #Max length name
        self.assertRaises(ValueError, lambda: user.addUser("the", "goodPassword", email="F" * 61)) #Min length email
        self.assertRaises(ValueError, lambda: user.addUser("dust", "goodPassword")) #Duplicate username
        otherUser = user.addUser("jimbo", "goodPassword")
        self.assertNotEqual(newUser.salt, otherUser.salt) #Check for proper salting
        self.assertNotEqual(newUser.password_hash, otherUser.password_hash) #Check for proper hashing

    def test_removeUser(self):
        testPerson = user.User.query.filter_by(username="jeff").first()
        user.removeUser(testPerson)
        self.assertIsNone(user.User.query.filter_by(username="jeff").first()) #Test remove by User object
        self.assertIsNotNone(user.User.query.filter_by(username="epicUsername69").first()) #Ensure random other users where not deleted
        user.removeUser("epicUsername69")
        self.assertIsNone(user.User.query.filter_by(username="epicUsername69").first()) #Test remove by username
        testPerson = user.User.query.filter_by(username="username").first()
        testEvent = event.createEvent("testEvent", testPerson.id, event.EventType.NOTE)
        self.assertIsNotNone(event.Event.query.filter_by(owner_id=testEvent.id).first())
        user.removeUser(testPerson.id)
        self.assertIsNone(user.User.query.filter_by(username="username").first()) #Test remove by id
        self.assertIsNone(event.Event.query.filter_by(id=testEvent.id).first())
        user.removeUser(testPerson.id) #Make sure error is not thrown for non existent user


    def test_authenticateUser(self):
        newUser = user.addUser("dust", "goodPassword")
        self.assertIsNone(user.authenticateUser("dust", "badPassword"))
        self.assertEqual(user.authenticateUser("dust", "goodPassword"), newUser)
        self.assertIsNone(user.authenticateUser("fakeUsername", "goodPassword"))

    def test_hashPassword(self):
        x = user.hashPassword("password", "ahhhhhhhhhhhhhhhhhhhh")
        self.assertEqual(x, "87944a379ba0ecdb9f65e2ddfea8503dd2fee42499d55ed590e9783a8c6d68b46e8a568146d1815e1b9330f6307cd0c101dc5330c6ef4b171b4a852efd037daa")
        x = user.hashPassword("password", "lessAHHHHH")
        self.assertNotEqual(x, "87944a379ba0ecdb9f65e2ddfea8503dd2fee42499d55ed590e9783a8c6d68b46e8a568146d1815e1b9330f6307cd0c101dc5330c6ef4b171b4a852efd037daa")
        self.assertEqual(len(x), 128)


if __name__ == '__main__':
    unittest.main()