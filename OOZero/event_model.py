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
    #children = db.relationship("Event", backref=db.backref("event", uselist=True), foreign_keys=[parent_id]) #TODO not working
    event_type = db.Column(db.Enum(EventType), unique=False, nullable=False)

    def __repr__(self):
        return str(self.id) + ', ' + str(self.name) + ', ' + str(self.owner_id) + ', ' + str(self.discrption)  + ', ' + str(self.timestamp)  + "\n" 

def createEvent(name, owner, event_type, discrption=None, start_time=None, end_time=None, parent=None):
    if name is None or 60 < len(name) or len(name) <= 0:
        raise ValueError("Name length out of range")
    if owner is None or user.getUser(owner) is None:
        raise ValueError("Must have a valid owner")
    if not type(event_type) is EventType:
        raise ValueError("Must have a valid event type")
    if not parent is None and Event.query.filter_by(id=parent).first() is None:
        raise ValueError("Parent, if used, must be a valid event")

    if event_type == EventType.NOTE and (not start_time is None or not end_time is None):
        raise ValueError("Note types do not have start or end times")
    elif event_type == EventType.REMINDER and (start_time is None or not end_time is None):
        raise ValueError("Reminder types have a start time and no end times")
    elif event_type == EventType.EVENT and (start_time is None or end_time is None):
        raise ValueError("Event types have start and end times")
    elif event_type == EventType.ALL_DAY and (start_time is None or end_time is None):
        raise ValueError("All day types have start and end times")

    db.session.add(Event(owner_id=owner, name=name, event_type=event_type, discrption=discrption, start_time=start_time, end_time=end_time, parent_id=parent))
    db.session.commit()
    return Event.query.filter_by(owner_id=owner, name=name, event_type=event_type, discrption=discrption, start_time=start_time, end_time=end_time, parent_id=parent).first()

