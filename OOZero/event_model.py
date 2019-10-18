from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db
import OOZero.user_model as user
import enum
import secrets
import datetime

class EventType(enum.Enum):
    NOTE = 1,
    EVENT = 2,
    ALL_DAY = 3,
    REMINDER = 4

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    owner = db.relationship("User", backref=db.backref("user", uselist=False))
    name = db.Column(db.String(60), unique=False, nullable=False)
    discrption = db.Column(db.Text, unique=False, nullable=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    start_time = db.Column(db.DateTime, unique=False, nullable=True)
    end_time = db.Column(db.DateTime, unique=False, nullable=True)
    parent = db.Column(db.Integer, unique=False, nullable=True)
    event_type = db.Column(db.Enum(EventType), unique=False, nullable=False)



