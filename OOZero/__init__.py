from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('OOZERO_CONFIG')


    from OOZero.model import db
    db.init_app(app)

    return app
