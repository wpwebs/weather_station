import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Query the database for all timestamps
query = 'SELECT timestamp FROM weather_data ORDER BY timestamp'
timestamps = pd.read_sql_query(query, conn)

# Convert timestamps to datetime
timestamps['timestamp'] = pd.to_datetime(timestamps['timestamp'])

# Calculate the difference between consecutive timestamps
timestamps['diff'] = timestamps['timestamp'].diff().dt.total_seconds()
print(timestamps)

# Close the database connection
conn.close()
