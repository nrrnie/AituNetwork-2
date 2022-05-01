from flask import Flask

from aituNetwork.auth import auth


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth, url_prefix='/auth')

    return app
