# data_processing.py

from sqlalchemy.orm import sessionmaker
from database_setup import SensorData, init_db

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

def save_sensor_data(sensor_type, value):
    new_data = SensorData(sensor_type=sensor_type, value=value)
    session.add(new_data)
    session.commit()

if __name__ == "__main__":
    # Beispiel: Simulierte Sensordaten speichern
    save_sensor_data('temperature', 23.5)
    save_sensor_data('humidity', 60.2)
    print("Beispieldaten gespeichert")
