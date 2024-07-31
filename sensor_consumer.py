# sensor_consumer.py

import pika
import json
from data_processing import save_sensor_data

def callback(ch, method, properties, body):
    data = json.loads(body)
    sensor_type = data['sensor_type']
    value = data['value']
    save_sensor_data(sensor_type, value)
    print(f" [x] Received {data}")

def consume_sensor_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_data')

    channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume_sensor_data()
