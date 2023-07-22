from sqlalchemy.sql import text

from wendy.application import db
from wendy.models.weekend import Weekend


def get_weekends(email: str):
    weekend_req = db.session.execute(text("SELECT * from weekend"))
    weekends = []
    for weekend_tuple in weekend_req:
        weekend = Weekend(
            id=weekend_tuple[0],
            name=weekend_tuple[1],
            address=weekend_tuple[2],
            date=weekend_tuple[3],
            participants=weekend_tuple[4],
            sharing_code=weekend_tuple[5],
        )
        participants = weekend.participants.split(";")
        if email in participants:
            weekends.append(
                {
                    "id": weekend.id,
                    "name": weekend.name,
                    "address": weekend.address,
                    "date": weekend.date,
                    "participants": participants,
                    "sharing_code": weekend.sharing_code,
                }
            )
    return weekends
