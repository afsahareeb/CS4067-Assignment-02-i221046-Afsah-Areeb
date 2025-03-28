from flask import Blueprint, request, jsonify
import requests
from model import mongo
from bson import ObjectId
from flask_cors import CORS
import pika
import json
from rabbitmq import send_notification
booking_bp = Blueprint("booking", __name__)
payment_bp = Blueprint("payment", __name__)

CORS(booking_bp)
CORS(payment_bp)

@booking_bp.route("/booking", methods=["POST"])
def create_booking():
    data = request.json
    print(f"Received booking request: {data}")  # Debugging line

    if mongo is None or mongo.db is None:
        print("MongoDB is NOT initialized properly!")  # Debugging
        return jsonify({"error": "Database connection issue"}), 500

    user_id = data.get("user_id")
    event_id = data.get("event_id")
    tickets = data.get("tickets")

    if not user_id or not event_id or not tickets:
        return jsonify({"error": "Missing required fields"}), 400
    

    # Check event availability
    event_response = requests.get(f"http://event-service:8000/events/{event_id}/availability")
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
    payment_response = requests.post("http://booking-service:5000/payments", json={
        "user_id": user_id,
        "amount": total_price

    })

    if payment_response.status_code != 200:
        return jsonify({"error": "Payment failed"}), 400
    
    payment_data = payment_response.json()
    user_email = payment_data.get("user_email", "unknown@example.com")

    booking = {
        "user_id": user_id,
        "event_id": event_id,
        "num_of_tickets": tickets,
        "booking_status": "confirmed",
        "total_price": total_price
    }

    # Now insert the booking into MongoDB
    inserted_booking = mongo.db.bookings.insert_one(booking)
    booking_id = str(inserted_booking.inserted_id)  # Convert ObjectId to string

    # Prepare notification message
    notification_data = {
        "user_id": user_id,
        "event_id": event_id,
        "booking_id": booking_id,
        "num_of_tickets": tickets,
        "total_price": total_price,
        "user_email": user_email
    }

    # Publish the message to RabbitMQ
    publish_message(notification_data)

    return jsonify({"message": "Booking successful", "booking_id": booking_id}), 201




@payment_bp.route("/payments", methods=["POST"])
def process_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    # Deduct balance from User Service (Mock)
    user_response = requests.post(f"http://user-service:8001/users/{user_id}/deduct_balance", json={
    "amount": amount
    })


    if user_response.status_code != 200:
        return jsonify({"error": "Insufficient balance for", "user_id": user_id, }), 400

    payment_data = user_response.json()
    user_email = payment_data.get("user_email", "unknown@example.com")  # Fallback if missing

    return jsonify({
        "message": "Balance deducted successfully",
        "user_id": user_id,
        "user_email": user_email,
        "deducted_amount": amount
    }), 200

@booking_bp.route("/booking/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    try:
        booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})

        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        # Convert ObjectId to string before returning
        booking["_id"] = str(booking["_id"])  
        return jsonify(booking), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

RABBITMQ_QUEUE = "booking_notifications"
def publish_message(message):
    """Function to publish messages to RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    channel.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=json.dumps(message))
    print(f" [x] Sent {message}")
    connection.close()