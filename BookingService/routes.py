from flask import Blueprint, request, jsonify
import requests
from model import mongo

booking_bp = Blueprint("booking", __name__)

payment_bp = Blueprint("payment", __name__)


@booking_bp.route("/booking", methods=["POST"])
def create_booking():
    data = request.json
    print(f"Received booking request: {data}")  # Debugging line

    user_id = data.get("user_id")
    event_id = data.get("event_id")
    tickets = data.get("tickets")

    if not user_id or not event_id or not tickets:
        return jsonify({"error": "Missing required fields"}), 400

    # Check event availability
    event_response = requests.get(f"http://127.0.0.1:8000/events/{event_id}/availability")
    if event_response.status_code != 200:
        print(f"Event Availability API Response: {event_response.status_code}, {event_response.text}")  # Debugging
        return jsonify({"error": "Event not found"}), 400

    event_data = event_response.json()
    available_tickets = event_data.get("available_tickets", 0)
    ticket_price = event_data.get("ticket_price", 0)

    if tickets > available_tickets:
        return jsonify({"error": "Not enough tickets available"}), 400

    total_price = tickets * ticket_price

    # Process payment with correct URL
    payment_response = requests.post("http://127.0.0.1:5000/payments", json={
        "user_id": user_id,
        "amount": total_price
    })

    if payment_response.status_code != 200:
        print(f"Payment API Response: {payment_response.status_code}, {payment_response.text}")  # Debugging
        return jsonify({"error": "Payment failed"}), 400

    # Create booking only if payment is successful
    booking = {
        "user_id": user_id,
        "event_id": event_id,
        "tickets": tickets,
        "status": "confirmed"
    }
    mongo.db.bookings.insert_one(booking)

    return jsonify({"message": "Booking successful", "booking": booking}), 201


@payment_bp.route("/payments", methods=["POST"])
def process_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    # Deduct balance from User Service (Mock)
    user_response = requests.post("http://127.0.0.1:8001/users/deduct_balance", json={
        "user_id": user_id,
        "amount": amount
    })

    if user_response.status_code != 200:
        return jsonify({"error": "Insufficient balance for", "user_id": user_id, }), 400

    return jsonify({"message": "Balance deducted successfully", "user_id": user_id,"deducted_amount": amount}), 200
