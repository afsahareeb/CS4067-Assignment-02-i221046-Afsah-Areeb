import pika
import json

def send_notification(booking_data):
    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='booking_notifications')

        # Convert booking data to JSON and publish to queue
        message = json.dumps(booking_data)
        channel.basic_publish(exchange='', routing_key='booking_notifications', body=message)

        print("Sent notification message to RabbitMQ:", message)

        # Close connection
        connection.close()
    except Exception as e:
        print(f"Error sending message to RabbitMQ: {str(e)}")
