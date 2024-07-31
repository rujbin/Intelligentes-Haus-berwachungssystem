from flask import Flask, render_template, jsonify
import random
import json

app = Flask(__name__)

def generate_data():
    """Generiert zufällige Sensordaten basierend auf der Konfiguration."""
    config = load_config()
    data = {
        "temperature": round(random.uniform(*config['temperature_range']), 2),
        "humidity": round(random.uniform(*config['humidity_range']), 2),
        "pressure": round(random.uniform(*config['pressure_range']), 2),
        "light_intensity": round(random.uniform(*config['light_intensity_range']), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False])
    }
    return data

def load_config(config_file='config.json'):
    """Lädt die Konfiguration aus einer JSON-Datei."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    """Gibt die generierten Sensordaten als JSON zurück."""
    data = generate_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
