import base64
import os
from flask import jsonify, request, send_file

from wendy.application import app
from wendy.application import db
from wendy.services import WeekendManager
from wendy.services.car_manager import CarManager
from wendy.services.user_manager import UserManager


weekend_manager = WeekendManager()
user_manager = UserManager()
car_manager = CarManager()

# User


@app.route("/createUser", methods=["POST"])
def create_user_route():
    try:
        return user_manager.create_user(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Weekends

@app.route("/createWeekend", methods=["POST"])
def create_weekend_route():
    try:
        return weekend_manager.create_weekend(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500        

@app.route("/joinWeekend", methods=["POST"])
def join_weekend_route():
    try:
        return weekend_manager.join_weekend(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500        


@app.route("/getWeekends", methods=["POST"])
def get_weekends_route():
    try:
        return weekend_manager.get_weekends(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


@app.route("/getWeekendById/<int:weekend_id>", methods=["GET"])
def get_weekend_by_id(weekend_id):
    try:
        return weekend_manager.get_weekend(weekend_id)
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


@app.route("/updateWeekend/<int:weekend_id>", methods=["PUT"])
def update_weekend(weekend_id):
    try:
        return weekend_manager.updateWeekendById(weekend_id, **request.get_json())
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
        return weekend_manager.updateWeekendPhotoById(weekend_id, image_filename)
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

@app.route("/updateWeekendPresence/<int:weekend_id>", methods=["PUT"])
def update_weekend_presence(weekend_id):
    try:
        return weekend_manager.updateWeekendPresenceById(weekend_id, **request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Car


@app.route("/createCar", methods=["POST"])
def create_car_route():
    try:
        return car_manager.create_car(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


@app.route("/getCarById/<int:car_id>", methods=["GET"])
def get_car_by_id(car_id):
    try:
        return car_manager.get_car(car_id=car_id)
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route("/updateCar/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    try:
        return car_manager.update_car_by_id(car_id, **request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


@app.route("/deleteCar/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    try:
        return car_manager.delete_car(car_id)
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route("/deleteUserFromCar/<int:car_id>", methods=["DELETE"])
def delete_user_from_car(car_id):
    try:
        return car_manager.delete_user_from_car(car_id=car_id, **request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route("/addUserToCar", methods=["POST"])
def add_user_to_car():
    try:
        return car_manager.add_user_to_car(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Crée les table dans sqlite
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=3000)
