import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
db = SQLAlchemy(app)
