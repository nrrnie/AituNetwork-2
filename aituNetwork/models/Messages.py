from aituNetwork.models import db
from datetime import datetime


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    message = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, index=True, nullable=False, default=datetime.now)
