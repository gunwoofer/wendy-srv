import shortuuid
from flask import jsonify

from sqlalchemy.sql import text

from wendy.application import db
from wendy.models.users_in_weekend import UsersInWeekend
from wendy.models.weekend import Weekend
from wendy.models.user import User


class WeekendManager:
    def __init__(self):
        pass

    def create_weekend(self, name: str, user_id: int):
        """
        creates a weekend
        :param name: the name of the weekend
        :param user_id: the id of the creator
        """
        weekend = Weekend(
            name=name,
            creator=user_id,
            sharing_code=shortuuid.ShortUUID().random(length=10),
        )
        db.session.add(weekend)
        db.session.commit()

        weekend_with_user = UsersInWeekend(weekend=weekend.id, user=user_id)
        db.session.add(weekend_with_user)
        db.session.commit()

        return self.get_weekend(weekend.id)

    def get_participants(self, weekend_id: int):
        """
        returns a list of participants in a weekend
        :param weekend_id: the id of the weekend
        """
        participants_req = db.session.execute(
            text("SELECT * from user WHERE user.id IN (SELECT user FROM users_in_weekend WHERE weekend = :weekend_id)"),
            {"weekend_id": weekend_id},
        )
        participants = [
            User(id=user[0], first_name=user[1], second_name=user[2], email=user[3]) for user in list(participants_req)
        ]
        participants = [participant.as_dict() for participant in participants]
        for participant in participants:
            is_present = db.session.execute(
                text("SELECT is_present FROM users_in_weekend WHERE weekend = :weekend_id AND user = :user_id"),
                {"weekend_id": weekend_id, "user_id": participant["id"]},
            )
            participant["is_present"] = list(is_present)[0][0]
        return participants

    def get_weekends(self, user_id: int):
        """
        returns a list of weekends
        :param user_id: the id of the user
        """
        weekend_req = db.session.execute(text("SELECT * from weekend"))
        weekends = []

        for weekend_tuple in weekend_req:
            weekend = Weekend(
                id=weekend_tuple.id,
                name=weekend_tuple.name,
                address=weekend_tuple.address,
                date_debut=weekend_tuple.date_debut,
                date_fin=weekend_tuple.date_fin,
                creator=weekend_tuple.creator,
                sharing_code=weekend_tuple.sharing_code,
                tricount_link=weekend_tuple.tricount_link,
                reservation_link=weekend_tuple.reservation_link,
            )

            participants = self.get_participants(weekend.id)
            if any(user_id == participant.get("id") for participant in participants):
                weekends.append(weekend.to_dict(participants))
        return weekends

    def get_weekend(self, weekend_id: int):
        """
        returns a weekend from is id
        :param weekend_id: the id of the weekend
        """
        weekend = Weekend.query.get(weekend_id)
        if not weekend:
            raise ValueError("Weekend not found")

        participants = self.get_participants(weekend_id)
        return weekend.to_dict(participants)

    def join_weekend(self, sharing_code: str, user_id: int):
        """
        joins a weekend
        :param sharing_code: the sharing code of the weekend
        :param user_id: the id of the user
        """
        weekends = list(Weekend.query.filter_by(sharing_code=sharing_code).all())
        if len(weekends) == 0:
            raise ValueError("Le weekend n'a pas ete trouve. Verifie le code du week end")
        else:
            weekend = weekends[0]
            participants = self.get_participants(weekend.id)
            if not any(user_id == participant.get("id") for participant in participants):
                weekend_with_user = UsersInWeekend(weekend=weekend.id, user=user_id)
                db.session.add(weekend_with_user)
                db.session.commit()
                return self.get_weekend(weekend.id)
            else:
                raise ValueError("Vous avez deja rejoint le weekend")

    def updateWeekendById(
        self,
        id: int,
        name: str = None,
        address: str = None,
        tricount_link: str = None,
        reservation_link: str = None,
        date_debut: str = None,
        date_fin: str = None,
    ):
        """
        Update a weekend from its id by data_weekend
        :param id: the id of the weekend
        :param name: the name of the weekend
        :param address: the address of the weekend
        :param tricount_link: the tricount link of the weekend
        :param reservation_link: the reservation link of the weekend
        :param date_debut: the start date of the weekend
        :param date_fin: the end date of the weekend
        """

        # Get the existing weekend record from the database
        weekend: Weekend = Weekend.query.get(id)
        if not weekend:
            raise ValueError("Weekend not found")

        # Update the weekend record with new data
        weekend.name = name if name else weekend.name
        weekend.address = address if address else weekend.address
        weekend.tricount_link = tricount_link if tricount_link else weekend.tricount_link
        weekend.reservation_link = reservation_link if reservation_link else weekend.reservation_link
        weekend.date_debut = date_debut if date_debut else weekend.date_debut
        weekend.date_fin = date_fin if date_fin else weekend.date_fin
        # Add more fields as needed...

        # Save the changes to the database
        db.session.commit()

        weekend_object = weekend.as_dict()
        participants = self.get_participants(weekend.id)
        weekend_object.update({"participants": participants})
        return weekend_object

    def updateWeekendPhotoById(self, id, path):
        # Get the existing weekend record from the database
        weekend: Weekend = Weekend.query.get(id)
        if not weekend:
            raise ValueError("Weekend not found")

        # Update the weekend record with new data
        weekend.photo_path = path

        # Save the changes to the database
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully."})

    def updateWeekendPresenceById(self, weekend_id: int, user_id: int, is_present: bool):
        """
        Update is_present of a user in a weekend
        :param weekend_id: the id of the weekend
        :param user_id: the id of the user
        :param is_present: the new value of is_present
        """
        weekend_with_user = UsersInWeekend.query.filter_by(weekend=weekend_id, user=user_id).first()
        if not weekend_with_user:
            raise ValueError("Weekend not found")
        weekend_with_user.is_present = is_present
        db.session.commit()
        return self.get_weekend(weekend_id)