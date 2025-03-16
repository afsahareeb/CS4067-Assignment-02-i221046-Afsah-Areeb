from fastapi import FastAPI, BackgroundTasks
from database import notifications_collection
from rabbitmq import get_channel
import json

app = FastAPI()

def send_email_notification(notification):
    print(f"Sending email: {notification}")
    # Add email sending logic here (e.g., using SMTP or SendGrid)

def callback(ch, method, properties, body):
    notification = json.loads(body)
    notifications_collection.insert_one(notification)
    send_email_notification(notification)

@app.on_event("startup")
def startup_event():
    channel = get_channel()
    channel.basic_consume(queue='booking_notifications', on_message_callback=callback, auto_ack=True)
    print("Notification Service is listening for messages...")
    channel.start_consuming()
