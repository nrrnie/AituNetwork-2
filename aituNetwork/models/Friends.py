from aituNetwork.models import db


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
