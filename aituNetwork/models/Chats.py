from aituNetwork.models import db


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def is_chat_exist(chat_id: int) -> bool:
        return Chats.query.get(chat_id) is not None
