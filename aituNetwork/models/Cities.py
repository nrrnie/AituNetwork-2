from aituNetwork.models import db


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    @staticmethod
    def get_cities():
        return Cities.query.order_by(Cities.id.asc()).all()

    @staticmethod
    def get_city(city_id: int):
        return Cities.query.get(city_id)
