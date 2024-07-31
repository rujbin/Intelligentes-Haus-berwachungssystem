import random
import time
import json
import logging
import pika

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file='config.json'):
    """Lädt die Konfiguration aus einer JSON-Datei."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Config file '{config_file}' not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the config file '{config_file}'.")
        raise

def generate_sensor_data(config):
    """Generiert zufällige Sensordaten basierend auf der Konfiguration."""
    data = {
        "temperature": round(random.uniform(*config['temperature_range']), 2),
        "humidity": round(random.uniform(*config['humidity_range']), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False]),
        "pressure": round(random.uniform(950, 1050), 2)  # Beispiel für einen neuen Sensor
    }
    return data

def send_to_rabbitmq(data, config):
    """Sendet die Sensordaten an RabbitMQ."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq_host']))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

        channel.basic_publish(exchange='',
                              routing_key='sensor_data',
                              body=json.dumps(data))
        logging.info(f"Sent data to RabbitMQ: {data}")
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")

def start_simulation(config):
    """Startet die Simulation der Sensordaten basierend auf der Konfiguration."""
    try:
        while True:
            data = generate_sensor_data(config)
            send_to_rabbitmq(data, config)
            time.sleep(config['sleep_time'])
    except KeyboardInterrupt:
        logging.info("Simulation stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        config = load_config()
        start_simulation(config)
    except Exception as e:
        logging.error(f"Failed to start simulation: {e}")
