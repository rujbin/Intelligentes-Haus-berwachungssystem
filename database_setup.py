import sqlite3
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_database(db_name='smart_home.db'):
    """Richtet die SQLite-Datenbank ein und erstellt die benötigten Tabellen."""
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Tabelle erstellen oder aktualisieren
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                motion BOOLEAN,
                smoke BOOLEAN,
                pressure REAL
            )
        ''')

        # Commit der Änderungen und Schließen der Verbindung
        conn.commit()
        logging.info("Database setup complete. Table created or updated successfully.")
    
    except sqlite3.Error as e:
        logging.error(f"An error occurred while setting up the database: {e}")
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
