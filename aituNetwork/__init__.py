from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask import Flask

from config import Config

db = SQLAlchemy()
ses = Session()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ses.init_app(app)

    with app.app_context():
        db.create_all()

    from aituNetwork.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from aituNetwork.main import main
    app.register_blueprint(main, url_prefix='')
    from aituNetwork.users import users
    app.register_blueprint(users, url_prefix='/users')

    return app
