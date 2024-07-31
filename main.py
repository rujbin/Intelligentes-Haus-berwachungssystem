import json

# Lesen der config.json-Datei
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json file not found.")
except json.JSONDecodeError:
    print("Error: config.json contains invalid JSON.")

# Zugriff auf Konfigurationswerte
temperature_range = config.get('temperature_range', [0, 0])
humidity_range = config.get('humidity_range', [0, 0])
pressure_range = config.get('pressure_range', [0, 0])
sleep_time = config.get('sleep_time', 1)
light_intensity_range = config.get('light_intensity_range', [0, 0])

# Beispiel für Verwendung der Konfiguration
print(f"Temperature range: {temperature_range}")
print(f"Humidity range: {humidity_range}")
print(f"Pressure range: {pressure_range}")
print(f"Sleep time: {sleep_time}")
print(f"Light intensity range: {light_intensity_range}")
