from flask import Flask

def create_app(config="OOZero.config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(config)

    from OOZero.model import db
    db.init_app(app)

    return app