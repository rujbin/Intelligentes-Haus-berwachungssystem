import sqlite3
import datetime

# Verbindung zu SQLite herstellen
try:
    conn = sqlite3.connect('smart_home.db')
    c = conn.cursor()

    # Tabelle erstellen
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            motion BOOLEAN,
            smoke BOOLEAN
        )
    ''')

    def save_data(data):
        try:
            data['timestamp'] = datetime.datetime.now().isoformat()
            c.execute('''
                INSERT INTO sensor_data (timestamp, temperature, humidity, motion, smoke)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['timestamp'], data['temperature'], data['humidity'], data['motion'], data['smoke']))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

    # Beispielhafte Datenspeicherung
    data = {
        "temperature": 22.5,
        "humidity": 45.2,
        "motion": True,
        "smoke": False
    }
    save_data(data)

except sqlite3.Error as e:
    print(f"An error occurred while connecting to the database: {e.args[0]}")
finally:
    if 'conn' in locals():
        conn.close()
