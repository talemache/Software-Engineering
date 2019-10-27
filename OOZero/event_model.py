from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db
import OOZero.user_model as user
import enum
import secrets
import datetime
import json
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64

class EventType(enum.Enum):
    NOTE = 1,
    EVENT = 2,
    ALL_DAY = 3,
    REMINDER = 4,
    ENCRYPTED = 5

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    owner = db.relationship("User", backref=db.backref("user"), foreign_keys=[owner_id], uselist=False)
    name = db.Column(db.String(60), unique=False, nullable=False)
    discrption = db.Column(db.Text, unique=False, nullable=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    start_time = db.Column(db.DateTime, unique=False, nullable=True)
    end_time = db.Column(db.DateTime, unique=False, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("event.id"), unique=False, nullable=True)
    parent = db.relationship("Event", remote_side=[id], uselist=False)
    #children = db.relationship("Event", backref=db.backref("event", uselist=True), foreign_keys=[parent_id]) #TODO not working
    event_type = db.Column(db.Enum(EventType), unique=False, nullable=False)

    def __repr__(self):
        return str(self.id) + ', ' + str(self.name) + ', ' + str(self.owner_id) + ', ' + str(self.discrption)  + ', ' + str(self.timestamp)  + "\n" 

def generateKey(value):
    """Generates a 256 bit encryption key off of the given string

    Args:
        value (str): string to derive key from

    Returns:
        (base64): 256 bit base64 string encryption key
    """
    hashFunct = hashlib.sha3_256()
    hashFunct.update(value.encode('utf-8'))
    return base64.urlsafe_b64encode(hashFunct.digest())

def encrypt(value, key):
    encryptionSuite = Fernet(generateKey(key))
    return encryptionSuite.encrypt(value.encode())

def decrypt(value, key):
    encryptionSuite = Fernet(generateKey(key))
    try:
        return encryptionSuite.decrypt(value).decode('utf-8')
    except InvalidToken:
        return None

def createEvent(name, owner, event_type, discrption=None, start_time=None, end_time=None, parent=None, password=None):
    if name is None or 60 < len(name) or len(name) <= 0:
        raise ValueError("Name length out of range")
    if owner is None or user.getUser(owner) is None:
        raise ValueError("Must have a valid owner")
    if not type(event_type) is EventType:
        raise ValueError("Must have a valid event type")
    if not parent is None and Event.query.filter_by(id=parent).first() is None:
        raise ValueError("Parent, if used, must be a valid event")
    if event_type == EventType.ENCRYPTED:
        if discrption is None:
            raise TypeError("Encrypted notes must have a discription")
        if password is None:
            raise TypeError("Encrypted notes must have a password")
    elif not password is None:
        raise TypeError("Only encrypted notes can have a password")

    if (event_type == EventType.NOTE or event_type == EventType.ENCRYPTED) and (not start_time is None or not end_time is None):
        raise ValueError("Note / encrypted note types do not have start or end times")
    elif event_type == EventType.REMINDER and (start_time is None or not end_time is None):
        raise ValueError("Reminder types have a start time and no end times")
    elif event_type == EventType.EVENT and (start_time is None or end_time is None):
        raise ValueError("Event types have start and end times")
    elif event_type == EventType.ALL_DAY and (start_time is None or end_time is None):
        raise ValueError("All day types have start and end times")

    if event_type == EventType.ENCRYPTED:
        discrption = encrypt(discrption, password)

    db.session.add(Event(owner_id=owner, name=name, event_type=event_type, discrption=discrption, start_time=start_time, end_time=end_time, parent_id=parent))
    db.session.commit()
    return Event.query.filter_by(owner_id=owner, name=name, event_type=event_type, discrption=discrption, start_time=start_time, end_time=end_time, parent_id=parent).first()

