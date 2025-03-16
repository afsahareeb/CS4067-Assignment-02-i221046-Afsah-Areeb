from flask_pymongo import PyMongo
mongo = PyMongo()

def init_db(app):
    global mongo
    mongo.init_app(app)
    print("MongoDB initialized successfully!")
