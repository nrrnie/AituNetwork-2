from aituNetwork.models import PostLikes, Friends
from aituNetwork.models import db
from datetime import datetime


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def get(post_id: int):
        return Posts.query.get(post_id)

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

    @staticmethod
    def delete_post(post_id: int):
        Posts.query.filter_by(id=post_id).delete()

        db.session.commit()

        PostLikes.delete_likes_from_post(post_id)

    @staticmethod
    def delete_posts_for_deleted_user(user_id: int):
        posts_id_list = Posts.query.filter_by(author_id=user_id).with_entities(Posts.id).all()
        Posts.query.filter_by(author_id=user_id).delete()

        return posts_id_list
