import pika
import json
import smtplib
from email.mime.text import MIMEText
from config import RABBITMQ_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD
from pymongo import MongoClient
from mongo import mongo

def send_email(to_email, subject, message):
    """Function to send emails"""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def callback(ch, method, properties, body):
    """Function to process messages from RabbitMQ"""
    data = json.loads(body)
    print("Received Notification:", data)

    # Store notification in MongoDB
    if mongo:
        mongo.db.notifications.insert_one(data)
        print("Notification stored in MongoDB")

    # Send email notification
    user_email = data.get("user_email")
    if user_email:
        subject = "Booking Confirmation"
        message = (
            f"Hello User {data.get('user_id')},\n\n"
            f"Your booking for Event {data.get('event_id')} is confirmed!\n\n"
            f"Booking ID: {data.get('booking_id')}\n"
            f"Total Tickets: {data.get('num_of_tickets')}\n"
            f"Total Price: ${data.get('total_price')}\n\n"
            "Thank you for using our service!"
        )

        send_email(user_email, subject, message)
    else:
        print("User email not found in message payload.")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    """Function to start RabbitMQ consumer"""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue="booking_notifications")

    channel.basic_consume(queue="booking_notifications", on_message_callback=callback)
    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
