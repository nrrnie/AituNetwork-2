from aituNetwork.models import db


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
