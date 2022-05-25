from aituNetwork.models import db


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
