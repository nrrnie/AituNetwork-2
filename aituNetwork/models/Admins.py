from aituNetwork.models import db


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)

    @staticmethod
    def is_admin(user_id: int):
        return Admins.query.filter_by(user_id=user_id).first() is not None
