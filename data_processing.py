import sqlite3
import json
import pika
import datetime
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Verbindung zur SQLite-Datenbank herstellen
def get_db_connection(db_name='smart_home.db'):
    """Stellt eine Verbindung zur SQLite-Datenbank her und gibt das Connection-Objekt zurück."""
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to SQLite: {e}")
        raise

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

def detect_anomalies(data):
    """Erkennt Anomalien in den Sensordaten."""
    anomalies = []
    if data.get('temperature') > 30:
        anomalies.append(f"High temperature detected: {data['temperature']}°C")
    if data.get('smoke'):
        anomalies.append("Smoke detected")
    if data.get('pressure') < 950 or data.get('pressure') > 1050:
        anomalies.append(f"Abnormal pressure detected: {data['pressure']} hPa")
    
    return anomalies

def process_data(ch, method, properties, body):
    """Verarbeitet empfangene Daten, erkennt Anomalien und speichert sie in der Datenbank."""
    conn = get_db_connection()
    try:
        data = json.loads(body)
        logging.info(f"Received data: {data}")
        
        anomalies = detect_anomalies(data)
        if anomalies:
            for anomaly in anomalies:
                logging.warning(f"Anomaly detected: {anomaly}")
        
        save_data(conn, data)
    
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logging.error(f"An error occurred while processing data: {e}")
    finally:
        conn.close()

def setup_rabbitmq():
    """Stellt die Verbindung zu RabbitMQ her und startet den Konsumenten."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        def callback(ch, method, properties, body):
            process_data(ch, method, properties, body)

        channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)
        logging.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")
    except KeyboardInterrupt:
        logging.info("Stopping consumer.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    setup_rabbitmq()
