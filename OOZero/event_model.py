from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db
import OOZero.user_model as user
import enum
import secrets
import datetime
import json

class EventType(enum.Enum):
    NOTE = 1,
    EVENT = 2,
    ALL_DAY = 3,
    REMINDER = 4

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
    #children = db.relationship("Event", remote_side=[id], uselist=True) #TODO not working
    event_type = db.Column(db.Enum(EventType), unique=False, nullable=False)

    def __repr__(self):
        return str(self.id) + ', ' + str(self.name) + ', ' + str(self.owner_id) + ', ' + str(self.discrption)  + ', ' + str(self.timestamp)  + "\n" 

def createEvent(name, owner, event_type, discrption=None, start_time=None, end_time=None, parent=None):
    pass