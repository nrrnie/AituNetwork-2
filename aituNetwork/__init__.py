from flask_session import Session, SqlAlchemySessionInterface
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import redirect, url_for
from flask import Flask

from config import Config

db = SQLAlchemy()
ses = Session()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

        ses.init_app(app)
        SqlAlchemySessionInterface(app, db, 'sessions', 'sess_')

    from aituNetwork.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from aituNetwork.main import main
    app.register_blueprint(main, url_prefix='')
    from aituNetwork.users import users
    app.register_blueprint(users, url_prefix='/users')
    from aituNetwork.utils import utils
    app.register_blueprint(utils, url_prefix='/utils')
    from aituNetwork.chat import chat
    app.register_blueprint(chat, url_prefix='/chat')

    from aituNetwork.template_functions import get_picture
    app.jinja_env.globals.update(get_picture=get_picture)

    from aituNetwork.template_functions import is_user_liked
    app.jinja_env.globals.update(is_user_liked=is_user_liked)

    from aituNetwork.template_functions import get_user
    app.jinja_env.globals.update(get_user=get_user)

    from aituNetwork.template_functions import get_second_chat_user
    app.jinja_env.globals.update(get_second_chat_user=get_second_chat_user)

    from aituNetwork.template_functions import get_last_message
    app.jinja_env.globals.update(get_last_message=get_last_message)

    @app.route('/')
    def main():
        return redirect(url_for('auth.login'))

    return app
