from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#TODO Add database URI to config/production and config/development config
#TODO Add username/password or secret key to instant/config
db = SQLAlchemy(app)

class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(30), unique=True, nullable=False)
    Name = db.Column(db.String(60), unique=False, nullable=True)
    Email = db.Column(db.String(60), unique=False, nullable=True)
    Hash = db.Column(db.String(64), unique=False, nullable=False)
    Salt = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return str(self.Username) + ' ' + str(self.Name) + ' ' + str(self.Email)