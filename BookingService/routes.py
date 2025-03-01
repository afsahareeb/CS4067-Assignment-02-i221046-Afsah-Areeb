from flask import Flask, request, jsonify
from database import db_session
from models import Booking
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://127.0.0.1:8001"
EVENT_SERVICE_URL = "http://127.0.0.1:8000"

@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.json
    user_id = data["user_id"]
    event_id = data["event_id"]
    tickets = data["tickets"]

    # ✅ Step 1: Check event availability
    event_response = requests.get(f"{EVENT_SERVICE_URL}/events/{event_id}/availability")
    if event_response.status_code != 200 or not event_response.json().get("available", False):
        return jsonify({"error": "Event is fully booked or unavailable"}), 400

    # ✅ Step 2: Calculate total price
    event_price = 50.0  # TODO: Fetch price dynamically from EventService
    total_price = event_price * tickets

    # ✅ Step 3: Check user's balance
    user_response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 400

    user_data = user_response.json()
    if user_data["balance"] < total_price:
        return jsonify({"error": "Insufficient balance"}), 400

    # ✅ Step 4: Deduct balance
    new_balance = user_data["balance"] - total_price
    requests.put(f"{USER_SERVICE_URL}/users/{user_id}/update_balance", json={"balance": new_balance})

    # ✅ Step 5: Create booking
    new_booking = Booking(user_id=user_id, event_id=event_id, tickets=tickets, total_price=total_price)
    db_session.add(new_booking)
    db_session.commit()

    return jsonify({"message": "Booking successful!", "booking_id": new_booking.id}), 201
