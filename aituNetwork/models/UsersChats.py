from aituNetwork.models import db
from aituNetwork.models import Chats


class UsersChats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    __table_args__ = (db.UniqueConstraint('chat_id', 'user_id'),)

    @staticmethod
    def is_user_in_chat(user_id: int, chat_id: int) -> bool:
        if not Chats.is_chat_exist(chat_id):
            return False

        if UsersChats.query.filter_by(chat_id=chat_id, user_id=user_id).first() is None:
            return False

        return True
