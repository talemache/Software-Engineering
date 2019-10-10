from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db

#TODO Add database URI to config/production and config/development config
#TODO Add username/password or secret key to instant/config


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(60), unique=False, nullable=True)
    email = db.Column(db.String(60), unique=False, nullable=True)
    password_hash = db.Column(db.String(64), unique=False, nullable=False)
    salt = db.Column(db.String(64), unique=False, nullable=False)
    profile_picture = db.Column(db.LargeBinary, nullable=True) 

    def __repr__(self):
        return str(self.id) + ', ' + str(self.username) + ', ' + str(self.name) + ', ' + str(self.email)  + ', ' + str(self.password_hash)  + ', ' + str(self.salt) + "\n" 

def addUser(user):
    """Make sure user parameters a valid and commit to database

    Args:
        user (User): Must have all required parameters of appropriate values

    Returns:
        on sucess - User: populated with the users infomation
        on failure - None: Null
    """
    pass

def authenticateUser(username, password):
    """Finds user with username and checks if hashed and salted password matches hash

    Args:
        username (str): username to search for. len < 30
        password (str): password to check

    Returns:
        on sucess - User: populated with the users infomation
        on failure - None: Null
    """
    pass

def removeUser(user):
    """Removes user from database

    Args:
        user (str | int | User): Removes user by id, username, or User object
    
    Returns:
        bool: was user sucessfuly removed
    """
    pass

def getUser(user):
    """Gets user from database

    Args:
        user (str | int): Finds user by id or username
    
    Returns:
        on sucess - User: populated with the users infomation
        on failure - None: Null
    """
    pass