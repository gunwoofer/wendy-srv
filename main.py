from flask import jsonify, request, send_file


from wendy.application import app
from wendy.application import db
from wendy.services.weekend import create_weekend
from wendy.services.weekend import join_weekend
from wendy.services.weekend import get_weekends
from wendy.services.weekend import get_weekend
from wendy.services.weekend import updateWeekendById, updateWeekendPhotoById
import base64
import os

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


@app.route('/updateWeekend/<int:weekend_id>', methods=['PUT'])
def update_weekend(weekend_id):
    try:
        return updateWeekendById(weekend_id, request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


def save_base64_image(base64_data, save_path):
    # Create the directory if it doesn't exist
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(base64_data))

@app.route("/upload_image/<int:weekend_id>", methods=["POST"])
def upload_image(weekend_id):
    try:
        data = request.json
        base64_image = data.get("base64_image")
        image_filename = "photo-weekend-" + str(weekend_id) + ".png"
        save_path = os.path.join(os.getcwd(), "uploads", image_filename)
        save_base64_image(base64_image, save_path)
        return updateWeekendPhotoById(weekend_id, image_filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_image/<int:weekend_id>", methods=["GET"])
def get_weekend_image_by_id(weekend_id):
    try:
        image_filename = "photo-weekend-" + str(weekend_id) + ".png"
        image_path = os.path.join(os.getcwd(), "uploads", image_filename)

        # Make sure the image file exists before sending it
        if not os.path.isfile(image_path):
            default_image_path = os.path.join(os.getcwd(), "default.png")
            return send_file(default_image_path, mimetype="image/png")


        # Use send_file to serve the image
        return send_file(image_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crée les table dans sqlite
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=3000)
