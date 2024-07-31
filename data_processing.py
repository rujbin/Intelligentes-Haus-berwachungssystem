import sqlite3
import json
import pika
import datetime

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('smart_home.db')
c = conn.cursor()

# Funktion zum Speichern von Daten in der Datenbank
def save_data(data):
    data['timestamp'] = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO sensor_data (timestamp, temperature, humidity, motion, smoke)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['timestamp'], data['temperature'], data['humidity'], data['motion'], data['smoke']))
    conn.commit()

# Beispiel für Datenverarbeitung und Anomalieerkennung
def process_data(data):
    # Beispielhafte Anomalieerkennung
    if data['temperature'] > 30:
        print(f"Anomaly detected: High temperature {data['temperature']}°C")
    
    if data['smoke']:
        print("Anomaly detected: Smoke detected")

    save_data(data)

# RabbitMQ-Konfiguration
def setup_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        def callback(ch, method, properties, body):
            data = json.loads(body)
            print(f"Received data: {data}")
            process_data(data)

        channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)
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

# Hauptprogramm
if __name__ == "__main__":
    setup_rabbitmq()
