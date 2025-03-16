from flask import Flask
from config import MONGO_URI
from model import init_db
from flask_cors import CORS
from routes import booking_bp
from routes import payment_bp

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI

CORS(app)

# Initialize MongoDB
init_db(app)

# Register Blueprints
app.register_blueprint(booking_bp)
app.register_blueprint(payment_bp)

if __name__ == "__main__":
    app.run(debug=True)
