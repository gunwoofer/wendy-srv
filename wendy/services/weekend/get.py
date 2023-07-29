from sqlalchemy.sql import text

from wendy.application import db
from wendy.models.weekend import Weekend


def get_weekends(email: str):
    weekend_req = db.session.execute(text("SELECT * from weekend"))
    weekends = []
    for weekend_tuple in weekend_req:
        weekend = Weekend(
            id=weekend_tuple.id,
            name=weekend_tuple.name,
            address=weekend_tuple.address,
            date_debut=weekend_tuple.date_debut,
            date_fin=weekend_tuple.date_fin,
            participants=weekend_tuple.participants,
            sharing_code=weekend_tuple.sharing_code,
            tricount_link=weekend_tuple.tricount_link,
            reservation_link=weekend_tuple.reservation_link
        )
        participants = weekend.participants.split(";")
        if email in participants:
            weekends.append(
                {
                    "id": weekend.id,
                    "name": weekend.name,
                    "address": weekend.address,
                    "date_debut": weekend.date_debut,
                    "date_fin": weekend.date_fin,
                    "participants": participants,
                    "sharing_code": weekend.sharing_code,
                    "tricount_link": weekend.tricount_link,
                    "reservation_link": weekend.reservation_link
                }
            )
    return weekends

def get_weekend(weekend_id):
    weekend = Weekend.query.get(weekend_id)
    if not weekend:
        raise ValueError("Weekend not found")

    participants = weekend.participants.split(";")
    weekend_data = Weekend(
        id= weekend.id,
        name= weekend.name,
        address= weekend.address,
        date_debut = weekend.date_debut,
        date_fin = weekend.date_fin,
        participants= participants,
        sharing_code= weekend.sharing_code,
        tricount_link= weekend.tricount_link,
        reservation_link= weekend.reservation_link
    )
    return weekend_data.as_dict()

