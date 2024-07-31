from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

def generate_data():
    data = {
        "temperature": round(random.uniform(15, 25), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "motion": random.choice([True, False]),
        "smoke": random.choice([True, False])
    }
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = generate_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
