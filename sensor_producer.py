# sensor_producer.py

import pika
import json

def send_sensor_data(sensor_type, value):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_data')

    message = {'sensor_type': sensor_type, 'value': value}
    channel.basic_publish(exchange='', routing_key='sensor_data', body=json.dumps(message))
    print(f" [x] Sent {message}")
    connection.close()

if __name__ == "__main__":
    # Beispiel: Simulierte Sensordaten senden
    send_sensor_data('temperature', 23.5)
    send_sensor_data('humidity', 60.2)
