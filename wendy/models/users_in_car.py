from wendy.application import db
from wendy.models.car import Car
from wendy.models.user import User


class UsersInCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car = db.Column(db.Integer, db.ForeignKey(Car.id), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_driver = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"UserInCar(car='{self.car}', user='{self.user}'"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
