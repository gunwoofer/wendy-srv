from wendy.application import db


class User(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User(first_name='{self.first_name}', second_name='{self.second_name}', email='{self.email}'"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
