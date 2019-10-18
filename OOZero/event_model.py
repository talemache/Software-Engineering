from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db
import enum
import secrets


class eventType(enum.Enum):
    NOTE = 1,
    EVENT = 2,
    ALL_DAY = 3,
    REMINDER = 4


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    discrption = db.Column(db.String(256), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    start_time = db.Column(db.DateTime, unique=False, nullable=True)
    end_time = db.Column(db.DateTime, unique=False, nullable=True)
    parent = db.Column(db.Integer, unique=False, nullable=True)
    event_type = db.Column(db.Enum(eventType), unique=False, nullable=False)


