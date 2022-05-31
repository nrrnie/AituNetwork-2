from aituNetwork.models import db, Friends
from datetime import datetime
from utils import random_id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, default=random_id)
    barcode = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    about_me = db.Column(db.String(255), nullable=False, default='Hi there! I\'m using AITU Network!')
    birthday = db.Column(db.String(255), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    hobbies = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True, default='Nur-Sultan (Astana)')
    program = db.Column(db.String(255), nullable=False, default='Computer Science')
    year = db.Column(db.Integer, nullable=False, default=1)
    group = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    registered = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    is_activated = db.Column(db.Boolean, nullable=False, default=False)
    last_online = db.Column(db.String(255), nullable=False, default=datetime.now)

    @staticmethod
    def get(user_id: int):
        return Users.query.get(user_id)

    @staticmethod
    def is_slug_taken(slug: str) -> bool:
        return Users.query.filter_by(slug=slug).first() is not None

    @staticmethod
    def update_user_info(user_id: int, update_info: dict):
        Users.query.filter_by(id=user_id).update(update_info)
        db.session.commit()

    @staticmethod
    def update_user_info_by_barcode(barcode: int, update_info: dict):
        Users.query.filter_by(barcode=barcode).update(update_info)
        db.session.commit()

    @staticmethod
    def get_users_for_new_friends_list(user_id: int):
        return Users.query.filter(Users.is_activated == 1, Users.id != user_id)
