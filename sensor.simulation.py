import random
import time
import json
from flask import Flask, jsonify

app = Flask(__name__)

def generate_sensor_data():
    data = {
        "temperature": round(random.uniform(15, 25), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False])
    }
    return data

@app.route('/sensor_data')
def sensor_data():
    data = generate_sensor_data()
    return jsonify(data)

def start_simulation():
    while True:
        data = generate_sensor_data()
        print(json.dumps(data))
        time.sleep(1)

if __name__ == "__main__":
    start_simulation()
