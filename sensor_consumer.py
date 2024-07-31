import pika
import json
import sqlite3
import datetime

# Verbindung zu SQLite-Datenbank herstellen
conn = sqlite3.connect('smart_home.db')
c = conn.cursor()

def save_data(data):
    data['timestamp'] = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO sensor_data (timestamp, temperature, humidity, motion, smoke)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['timestamp'], data['temperature'], data['humidity'], data['motion'], data['smoke']))
    conn.commit()

def process_data(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received data: {data}")
    save_data(data)

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')
        channel.basic_consume(queue='sensor_data', on_message_callback=process_data, auto_ack=True)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
    except KeyboardInterrupt:
        print("Stopping consumer.")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
        conn.close()

if __name__ == "__main__":
    main()
