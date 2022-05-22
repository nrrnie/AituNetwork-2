from aituNetwork import db

from datetime import datetime
from random import randint


def random_id():
    mn = 1000000
    mx = 9999999

    rand = randint(mn, mx)
    while Users.query.filter_by(id=rand).first() is not None:
        rand = randint(mn, mx)

    return rand


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, default=random_id)
    barcode = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    about_me = db.Column(db.String(255), nullable=False, default='Hi there! I\'m using AITU Network!')
    password = db.Column(db.String(255), nullable=False)
    registered = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    is_activated = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def is_slug_taken(slug: str) -> bool:
        return Users.query.filter_by(slug=slug).first() is not None

    @staticmethod
    def update_user_info(user_id: int, update_info: dict):
        Users.query.filter_by(id=user_id).update(update_info)
        db.session.commit()


class ProfilePictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    added = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def get_profile_picture(user_id: int):
        return ProfilePictures.query.filter_by(user_id=user_id).order_by(ProfilePictures.id.desc()).first()


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    friend_id = db.Column(db.Integer, index=True, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id'),)

    @staticmethod
    def add_friend(user_id: int, friend_id: int):
        if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is None:
            friend = Friends(user_id=user_id, friend_id=friend_id)
            db.session.add(friend)
            db.session.commit()

    @staticmethod
    def remove_friend(user_id: int, friend_id: int):
        if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is not None:
            Friends.query.filter_by(user_id=user_id, friend_id=friend_id).delete()
            db.session.commit()

    @staticmethod
    def get_friend_status(user_id: int, friend_id: int) -> int:
        is_my_friend = Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        am_i_friend = Friends.query.filter_by(user_id=friend_id, friend_id=user_id).first()

        # friend_status
        # 1: I sent request
        # 2: Profile user sent request
        # 3: Friends

        friend_status = None
        if is_my_friend is not None and am_i_friend is not None:
            friend_status = 3
        elif is_my_friend is not None:
            friend_status = 1
        elif am_i_friend is not None:
            friend_status = 2

        return friend_status


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def add_post(user_id: int, content: str):
        post = Posts(user_id=user_id, content=content)
        db.session.add(post)
        db.session.commit()
