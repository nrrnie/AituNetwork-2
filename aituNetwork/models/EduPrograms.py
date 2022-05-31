from aituNetwork.models import db


class EduPrograms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    @staticmethod
    def get_edu_program(edu_program_id: int):
        return EduPrograms.query.get(edu_program_id)

    @staticmethod
    def get_edu_programs():
        return EduPrograms.query.order_by(EduPrograms.id.asc()).all()
