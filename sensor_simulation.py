import random
import time
import json
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file='config.json'):
    """Lädt die Konfiguration aus einer JSON-Datei."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def generate_sensor_data(config):
    """Generiert zufällige Sensordaten basierend auf der Konfiguration."""
    data = {
        "temperature": round(random.uniform(*config['temperature_range']), 2),
        "humidity": round(random.uniform(*config['humidity_range']), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False])
    }
    return data

def start_simulation(config):
    """Startet die Simulation der Sensordaten basierend auf der Konfiguration."""
    try:
        while True:
            data = generate_sensor_data(config)
            logging.info(f"Generated data: {json.dumps(data)}")
            time.sleep(config['sleep_time'])
    except KeyboardInterrupt:
        logging.info("Simulation stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    config = load_config()
    start_simulation(config)
