# Basic user session management code.
from flask import Flask, redirect, url_for, session
from functools import wraps

def login_required(func):
    """Decorator function to wrap each function that requires user login. 
       Redirects to '/login' if no user is logged in.
    """
    @wraps(func)
    def decorator():
        if not 'user' in session:
            return redirect(url_for('login'))
        return func()
    return decorator

def user_login(user):
    """Logs this user in and saves their information in session

    Args:
        user: Value returned by authenticateUser()
    """
    session['user'] = user.username

def user_logout():
    """Log the current user out"""
    if 'user' in session:
        del session['user']
