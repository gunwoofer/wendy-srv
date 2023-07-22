import os
from datetime import datetime
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
db = SQLAlchemy(app)


@app.route("/createWeekend", methods=["POST"])
def create_weekend():
    data = request.get_json()
    name = data.get("name")
    creator = data.get("creator")
    weekend = Weekend(name=name, participants=creator)
    db.session.add(weekend)
    db.session.commit()
    return weekend.as_dict()


@app.route("/getWeekends", methods=["POST"])
def get_weekends():
    data = request.get_json()
    email = data.get("email")
    weekends = Weekend.query.filter_by(participants=email).all()
    weekend_list = []
    for weekend in weekends:
        weekend_list.append(
            {
                "id": weekend.id,
                "name": weekend.name,
                "address": weekend.address,
                "date": weekend.date,
                "participants": weekend.participants,
            }
        )
    return jsonify(weekend_list)


class Weekend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    participants = db.Column(db.String(200))

    def __repr__(self):
        return f"Weekend(name='{self.name}', address='{self.address}', date='{self.date}', participants='{self.participants}')"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Crée les table dans sqlite
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=3000)
