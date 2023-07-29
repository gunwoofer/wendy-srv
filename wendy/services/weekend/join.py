from wendy.application import db
from wendy.models.weekend import Weekend


def join_weekend(sharing_code: str, user: str):
    weekends = Weekend.query.filter_by(sharing_code=sharing_code).all()
    if len(weekends) == 0:
        raise ValueError("Le weekend n'a pas ete trouve. Verifie le code du week end")
    else:
        for weekend in weekends:
            if user not in weekend.participants.split(";"):
                weekend.participants += f";{user}"
                db.session.merge(weekend)
                db.session.commit()
                weekend = Weekend(
                    id=weekend.id,
                    name=weekend.name,
                    address=weekend.address,
                    date_debut=weekend.date_debut,
                    date_fin=weekend.date_fin,
                    participants=weekend.participants.split(";"),
                    sharing_code=weekend.sharing_code,
                )
                return weekend.as_dict()
            else:
                raise ValueError("Vous avez deja rejoint le weekend")
