from wendy.application import db
from wendy.models.user import User


class UserManager:
    def __init__(self):
        pass

    def create_user(self, first_name: str, second_name: str, email: str):
        user = User(
            first_name=first_name,
            second_name=second_name,
            email=email,
        )
        db.session.add(user)
        db.session.commit()
        return user.as_dict()
