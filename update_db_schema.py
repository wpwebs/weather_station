import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create weather_data table if it does not exist, including new fields
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    temperature FLOAT,
                    humidity INTEGER,
                    wind_speed FLOAT,
                    wind_direction INTEGER,
                    solar_radiation FLOAT,
                    uv_index FLOAT,
                    indoor_temperature FLOAT,
                    indoor_humidity INTEGER,
                    outdoor_feels_like FLOAT)''')

# Create a table to store the latest timestamp
cursor.execute('''CREATE TABLE IF NOT EXISTS latest_timestamp (
                    id INTEGER PRIMARY KEY,
                    last_update DATETIME)''')

# Initialize the latest_timestamp table if it's empty
cursor.execute('''INSERT OR IGNORE INTO latest_timestamp (id, last_update)
                  VALUES (1, '2024-07-26 00:00:00')''')

conn.commit()
conn.close()

