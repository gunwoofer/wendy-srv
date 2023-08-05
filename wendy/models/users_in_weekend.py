from wendy.application import db
from wendy.models.weekend import Weekend
from wendy.models.user import User


class UsersInWeekend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekend = db.Column(db.Integer, db.ForeignKey(Weekend.id), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_present = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"UserInWeekend(weekend='{self.weekend}', user='{self.user}', is_present='{self.is_present}'"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
