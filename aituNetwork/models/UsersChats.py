from aituNetwork.models import db


class UsersChats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    __table_args__ = (db.UniqueConstraint('chat_id', 'user_id'),)
