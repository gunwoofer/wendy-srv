import shortuuid

from wendy.application import db
from wendy.models.weekend import Weekend


def create_weekend(
    name: str,
    creator: str,
):
    weekend = Weekend(
        name=name,
        participants=creator,
        sharing_code=shortuuid.ShortUUID().random(length=10),
    )
    db.session.add(weekend)
    db.session.commit()
    weekend.participants = weekend.participants.split(";")
    return weekend.as_dict()
