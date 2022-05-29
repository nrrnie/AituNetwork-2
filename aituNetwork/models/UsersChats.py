from aituNetwork.models import db
from aituNetwork.models import Chats
from typing import Union


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

    @staticmethod
    def get_second_chat_user(chat_id: int, user_id: int) -> Union[int, None]:
        chat = Chats.query.get(chat_id)

        if chat is None:
            return chat

        chat_user = UsersChats.query.filter(UsersChats.chat_id == chat_id, UsersChats.user_id != user_id).first()
        return chat_user if chat_user is None else chat_user.user_id

    @staticmethod
    def get_user_chats(user_id: int) -> list:
        chats = UsersChats.query.filter_by(user_id=user_id).all()

        return chats
