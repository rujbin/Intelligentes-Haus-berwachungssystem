import pika
import json
import sqlite3
import datetime
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Verbindung zu SQLite-Datenbank herstellen
def create_table(conn):
    """Stellt sicher, dass die Tabelle in der Datenbank vorhanden ist."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                motion BOOLEAN,
                smoke BOOLEAN,
                pressure REAL
            )
        ''')

def save_data(conn, data):
    """Speichert die Sensordaten in der SQLite-Datenbank."""
    data['timestamp'] = datetime.datetime.now().isoformat()
    try:
        with conn:
            conn.execute('''
                INSERT INTO sensor_data (timestamp, temperature, humidity, motion, smoke, pressure)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['timestamp'], data.get('temperature'), data.get('humidity'), data.get('motion'), data.get('smoke'), data.get('pressure')))
        logging.info(f"Saved data to SQLite: {data}")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while saving data: {e}")

def process_data(ch, method, properties, body, conn):
    """Verarbeitet empfangene Daten und speichert sie in der Datenbank."""
    try:
        data = json.loads(body)
        logging.info(f"Received data: {data}")
        save_data(conn, data)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logging.error(f"An error occurred while processing data: {e}")

def main():
    """Hauptfunktion zum Starten des Consumers."""
    try:
        # Verbindung zu SQLite-Datenbank herstellen
        conn = sqlite3.connect('smart_home.db')
        create_table(conn)

        # Verbindung zu RabbitMQ herstellen
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        def callback(ch, method, properties, body):
            process_data(ch, method, properties, body, conn)

        channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)
        logging.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")
    except sqlite3.Error as e:
        logging.error(f"Error connecting to SQLite: {e}")
    except KeyboardInterrupt:
        logging.info("Stopping consumer.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
