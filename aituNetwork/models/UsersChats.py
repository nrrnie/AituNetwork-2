from sqlalchemy import func, desc
from aituNetwork.models import db, Chats, Messages
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
        chat = Chats.get(chat_id)

        if chat is None:
            return chat

        chat_user = UsersChats.query.filter(UsersChats.chat_id == chat_id, UsersChats.user_id != user_id).first()
        return chat_user if chat_user is None else chat_user.user_id

    @staticmethod
    def get_user_chats(user_id: int):
        chat_id_list = UsersChats.query.filter_by(user_id=user_id).with_entities(UsersChats.chat_id)
        chats = Messages.query.filter(Messages.chat_id.in_(chat_id_list)).group_by(Messages.chat_id).with_entities(func.max(Messages.id).label('id'), Messages.chat_id).order_by(desc('id')).all()

        return chats

    @staticmethod
    def get_chat_between_users(first_user_id: int, second_user_id: int) -> Union[int, None]:
        second_user_id_chats = UsersChats.query.filter_by(user_id=second_user_id).with_entities(UsersChats.chat_id)
        chat = UsersChats.query.filter(UsersChats.chat_id.in_(second_user_id_chats),
                                       UsersChats.user_id == first_user_id).first()

        return chat if chat is None else chat.chat_id

    @staticmethod
    def add_user_to_chat(chat_id: int, user_id: int):
        user_chat = UsersChats(chat_id=chat_id, user_id=user_id)
        db.session.add(user_chat)
        db.session.commit()

    @staticmethod
    def delete_chats_for_deleted_user(user_id: int):
        chat_list = UsersChats.get_user_chats(user_id)
        for chat in chat_list:
            UsersChats.query.filter_by(chat_id=chat.chat_id).delete()

        return chat_list
