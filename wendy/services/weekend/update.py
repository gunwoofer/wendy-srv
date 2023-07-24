from wendy.application import db
from wendy.models.weekend import Weekend

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
    # Add more fields as needed...

    # Save the changes to the database
    db.session.commit()

    return weekend.as_dict();