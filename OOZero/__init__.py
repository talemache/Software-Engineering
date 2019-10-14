from flask import Flask

# def create_app(config="OOZero.config.ProductionConfig"):
def create_app(config="OOZero.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)

    app.secret_key = b'35f9aefeaaf1094198411e88c97a731675c2e6544c10cbfcd8392db338a292f1'

    from OOZero.model import db
    db.init_app(app)

    return app
