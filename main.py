from flask import jsonify, request


from wendy.application import app
from wendy.application import db
from wendy.services.weekend import create_weekend
from wendy.services.weekend import join_weekend
from wendy.services.weekend import get_weekends
from wendy.services.weekend import get_weekend


@app.route("/createWeekend", methods=["POST"])
def create_weekend_route():
    data = request.get_json()
    name = data.get("name")
    creator = data.get("creator")
    return create_weekend(name, creator)


@app.route("/joinWeekend", methods=["POST"])
def join_weekend_route():
    data = request.get_json()
    name = data.get("name")
    creator = data.get("creator")
    try:
        return join_weekend(sharing_code=name, user=creator)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/getWeekends", methods=["POST"])
def get_weekends_route():
    data = request.get_json()
    email = data.get("email")
    weekends = get_weekends(email)
    return jsonify(weekends)

@app.route('/getWeekendById/<int:weekend_id>', methods=['GET'])
def get_weekend_by_id(weekend_id):
    try:
        return get_weekend(weekend_id=weekend_id)
    except Exception as e:
        return jsonify({"error": str(e)})

# Crée les table dans sqlite
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=3000)
