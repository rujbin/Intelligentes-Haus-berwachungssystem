import pika
import json
import random
import time
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_sensor_data():
    """Generiert zufällige Sensordaten einschließlich neuer Sensoren."""
    data = {
        "temperature": round(random.uniform(15, 25), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False]),
        "pressure": round(random.uniform(950, 1050), 2)  # Neuer Sensor
    }
    return data

def main():
    """Hauptfunktion zum Starten des Produzenten."""
    config = {
        'rabbitmq_host': 'localhost'  # Konfiguriere hier den RabbitMQ-Host
    }
    
    try:
        # Verbindung zu RabbitMQ herstellen
        connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq_host']))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        while True:
            data = generate_sensor_data()
            channel.basic_publish(exchange='',
                                  routing_key='sensor_data',
                                  body=json.dumps(data))
            logging.info(f"Sent data to RabbitMQ: {data}")
            time.sleep(1)  # Pause zwischen den Sendungen

    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")
    except KeyboardInterrupt:
        logging.info("Stopping producer.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    main()
