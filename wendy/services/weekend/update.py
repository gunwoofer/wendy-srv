from wendy.application import db
from wendy.models.weekend import Weekend
from flask import jsonify

def updateWeekendById(id, data_weekend):
    # Get the existing weekend record from the database
    weekend: Weekend = Weekend.query.get(id)
    if not weekend:
        raise ValueError("Weekend not found")

    # Update the weekend record with new data
    if 'name' in data_weekend:
        weekend.name = data_weekend['name']
    if 'address' in data_weekend:
        weekend.address = data_weekend['address']
    if 'tricount_link' in data_weekend:
        weekend.tricount_link = data_weekend['tricount_link']
    if 'reservation_link' in data_weekend:
        weekend.reservation_link = data_weekend['reservation_link']
    if 'date_debut' in data_weekend:
        weekend.date_debut = data_weekend['date_debut']
    if 'date_fin' in data_weekend:
        weekend.date_fin = data_weekend['date_fin']
    # Add more fields as needed...

    # Save the changes to the database
    db.session.commit()

    weekend_object = weekend.as_dict()
    weekend_object.update({"participants": weekend.participants.split(';')})
    return weekend_object

def updateWeekendPhotoById(id, path):
    # Get the existing weekend record from the database
    weekend: Weekend = Weekend.query.get(id)
    if not weekend:
        raise ValueError("Weekend not found")

    # Update the weekend record with new data
    weekend.photo_path = path

    # Save the changes to the database
    db.session.commit()

    return jsonify({"message": "Image uploaded successfully."})