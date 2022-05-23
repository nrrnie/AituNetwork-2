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
    def get_friend_list(user_id: int):
        return Friends.query.filter(
            Friends.user_id.in_(
                Friends.query.filter_by(user_id=user_id).with_entities(Friends.friend_id)
            ),
            Friends.friend_id == user_id
        ).all()

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
    author_id = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def add_post(author_id: int, content: str):
        post = Posts(author_id=author_id, content=content)
        db.session.add(post)
        db.session.commit()

    @staticmethod
    def get_posts(author_id: int):
        posts = Posts.query.filter_by(author_id=author_id).order_by(Posts.id.desc()).all()
        for post in posts:
            post.likes = PostLikes.get_like_counts(post.id)
        return posts

    @staticmethod
    def get_feed(user_id: int):
        friend_list = [friend.user_id for friend in Friends.get_friend_list(user_id)]

        # Also show content of user
        friend_list.append(user_id)

        posts = Posts.query.filter(Posts.author_id.in_(friend_list)).order_by(Posts.id.desc()).all()
        for post in posts:
            post.likes = PostLikes.get_like_counts(post.id)

        return posts


class PostLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    post_id = db.Column(db.Integer, index=True, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)

    @staticmethod
    def get_like_counts(post_id: int):
        return PostLikes.query.filter_by(post_id=post_id).count()

    @staticmethod
    def add(user_id: int, post_id: int):
        post_like = PostLikes(user_id=user_id, post_id=post_id)
        db.session.add(post_like)
        db.session.commit()

    @staticmethod
    def get_post_like(user_id: int, post_id: int):
        return PostLikes.query.filter_by(user_id=user_id, post_id=post_id).first()

    @staticmethod
    def remove(user_id: int, post_id: int):
        post_like = PostLikes.get_post_like(user_id, post_id)
        db.session.delete(post_like)
        db.session.commit()
