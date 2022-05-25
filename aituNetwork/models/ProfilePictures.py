from aituNetwork.models import db
from datetime import datetime


class ProfilePictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    added = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def get_profile_picture(user_id: int):
        return ProfilePictures.query.filter_by(user_id=user_id).order_by(ProfilePictures.id.desc()).first()
