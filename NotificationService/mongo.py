from flask_pymongo import PyMongo
from config import MONGO_URI
from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)  # Ensure this is initialized
