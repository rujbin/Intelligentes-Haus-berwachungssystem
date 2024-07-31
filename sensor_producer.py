import pika
import json
import random
import time

def generate_sensor_data():
    data = {
        "temperature": round(random.uniform(15, 25), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False])
    }
    return data

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        while True:
            data = generate_sensor_data()
            channel.basic_publish(exchange='',
                                  routing_key='sensor_data',
                                  body=json.dumps(data))
            print(f"Sent data: {data}")
            time.sleep(1)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
    except KeyboardInterrupt:
        print("Stopping producer.")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    main()
