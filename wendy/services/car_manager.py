from sqlalchemy import text
from wendy.application import db
from wendy.models.car import Car
from wendy.models.user import User
from wendy.models.users_in_car import UsersInCar


class CarManager:
    def __init__(self):
        pass

    def create_car(
        self,
        user_id: int,
        name: str,
        max_person: str,
        matricule: str = None,
        start_hour: str = None,
        start_address: str = None,
    ):
        """
        creates a car
        :param user_id: the id of the creator
        :param name: the name of the car
        :param max_person: the max number of person in the car
        :param matricule: the matricule of the car
        :param start_hour: the hour of departure
        :param start_address: the address of departure
        """
        car = Car(
            matricule=matricule,
            name=name,
            max_person=max_person,
            start_hour=start_hour,
            start_address=start_address,
        )
        db.session.add(car)
        db.session.commit()

        car_with_user = UsersInCar(car=car.id, user=user_id, is_driver=True)
        db.session.add(car_with_user)
        db.session.commit()
        return car.to_dict(self.get_participants(car.id))

    def get_participants(self, car_id: int):
        """
        returns a list of participants in a car
        :param car_id: the id of the car
        """
        participants_req = db.session.execute(
            text("SELECT * from user WHERE user.id IN (SELECT user FROM users_in_car WHERE car = :car_id)"),
            {"car_id": car_id},
        )
        participants = [
            User(id=user[0], first_name=user[1], second_name=user[2], email=user[3]) for user in list(participants_req)
        ]
        return [participant.as_dict() for participant in participants]

    def get_car(self, car_id: int):
        """
        returns a car from its id
        :param car_id: the id of the car
        """
        car = Car.query.filter_by(id=car_id).first()
        participants = self.get_participants(car_id)

        return car.to_dict(participants)

    def add_user_to_car(self, user_id: int, car_id: int):
        """
        adds a user to a car
        :param user_id: the id of the user
        :param car_id: the id of the car
        """
        car_with_user = UsersInCar(car=car_id, user=user_id, is_driver=False)
        db.session.add(car_with_user)
        db.session.commit()
        return self.get_car(car_id)

    def delete_user_from_car(self, user_id: int, car_id: int):
        """
        deletes a user from a car
        :param user_id: the id of the user
        :param car_id: the id of the car
        """
        car_with_user = UsersInCar.query.filter_by(car=car_id, user=user_id).first()
        db.session.delete(car_with_user)
        db.session.commit()
        return self.get_car(car_id)

    def update_car_by_id(
        self,
        car_id: int,
        matricule: str = None,
        name: str = None,
        max_person: str = None,
        start_hour: str = None,
        start_address: str = None,
    ):
        """
        updates a car
        :param car_id: the id of the car
        :param matricule: the matricule of the car
        :param name: the name of the car
        :param max_person: the max number of person in the car
        :param start_hour: the hour of departure
        :param start_address: the address of departure
        """
        car = Car.query.filter_by(id=car_id).first()
        car.matricule = matricule if matricule else car.matricule
        car.name = name if name else car.name
        car.max_person = max_person if max_person else car.max_person
        car.start_hour = start_hour if start_hour else car.start_hour
        car.start_address = start_address if start_address else car.start_address
        db.session.commit()
        return car.to_dict(self.get_participants(car_id))

    def delete_car(self, car_id: int):
        """
        deletes a car
        :param car_id: the id of the car
        """
        car = Car.query.filter_by(id=car_id).first()
        db.session.delete(car)
        db.session.commit()
        return car.as_dict()
    
    def update_driver_in_car(self, car_id: int, user_id: str, is_driver: bool):
        user_in_car = UsersInCar.query.filter_by(car=car_id, user=user_id)
        user_in_car.is_driver = is_driver
        db.session.commit()
        return self.get_car(car_id)
