from wendy.application import db
from wendy.models.weekend import Weekend


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    max_person = db.Column(db.Integer, nullable=False)
    matricule = db.Column(db.String(30))
    start_hour = db.Column(db.String(200))
    start_address = db.Column(db.String(200))
    weekend_id = db.Column(db.Integer, db.ForeignKey(Weekend.id), nullable=False)

    def __repr__(self):
        return f"name='{self.second_name}', max_person='{self.email}' Car(matricule='{self.first_name}', start_hour='{self.start_hour}', start_address='{self.start_address}', weekend_id='{self.weekend_id}'"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_dict(self, participants):
        car = self.as_dict()
        car["participants"] = participants
        return car
