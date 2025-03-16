from flask_pymongo import PyMongo
from config import MONGO_URI

mongo = None

def init_db():
    global mongo
    from flask import Flask
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI
    mongo = PyMongo(app)
