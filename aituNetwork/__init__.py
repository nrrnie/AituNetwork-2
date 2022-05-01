from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from config import Config

from aituNetwork.auth import auth


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth, url_prefix='/auth')

    return app
