# database_setup.py

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True)
    sensor_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    engine = create_engine('sqlite:///sensor_data.db')
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    engine = init_db()
    print("Datenbank und Tabellen erstellt")
