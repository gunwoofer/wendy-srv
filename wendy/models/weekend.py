from wendy.application import db
from wendy.models.user import User


class Weekend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    # date = db.Column(db.DateTime, default=datetime.utcnow)
    date_debut = db.Column(db.String(200))
    date_fin = db.Column(db.String(200))
    creator = db.Column(db.String(200), db.ForeignKey(User.id), nullable=False)
    sharing_code = db.Column(db.String(10))
    tricount_link = db.Column(db.String(200))
    reservation_link = db.Column(db.String(200))
    photo_path = db.Column(db.String(200))

    def __repr__(self):
        return f"Weekend(name='{self.name}', address='{self.address}', date_debut='{self.date_debut}', date_fin='{self.date_fin}', creator='{self.creator}', sharing_code='{self.sharing_code}')"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_dict(self, participants, cars):
        weekend = self.as_dict()
        weekend["participants"] = participants
        weekend["cars"] = cars
        return weekend
