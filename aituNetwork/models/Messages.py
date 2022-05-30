from aituNetwork.models import db
from datetime import datetime


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    message = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, index=True, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'message': self.message,
            'created': self.created.__str__()
        }

    @staticmethod
    def get_messages(chat_id: int, offset: int, limit: int):
        messages = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).limit(limit).offset(offset)

        return messages.all()

    @staticmethod
    def get_last_message(chat_id: int):
        return Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).first()
