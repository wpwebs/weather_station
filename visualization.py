import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query data from the database
query = '''
SELECT timestamp, temperature, humidity, wind_speed, wind_direction,
       solar_radiation, uv_index, indoor_temperature, indoor_humidity, outdoor_feels_like
FROM weather_data
ORDER BY timestamp
'''
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Convert timestamps to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Remove duplicate entries
df = df.drop_duplicates(subset='timestamp')

# Plot the data
plt.figure(figsize=(15, 12))

# Plot outdoor temperature and feels like temperature
plt.subplot(4, 1, 1)
plt.plot(df['timestamp'], df['temperature'], label='Outdoor Temperature (°F)', color='orange')
plt.plot(df['timestamp'], df['outdoor_feels_like'], label='Outdoor Feels Like (°F)', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°F)')
plt.title('Outdoor Temperature and Feels Like Temperature Over Time')
plt.legend()
plt.grid(True)

# Plot indoor temperature
plt.subplot(4, 1, 2)
plt.plot(df['timestamp'], df['indoor_temperature'], label='Indoor Temperature (°F)', color='blue')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°F)')
plt.title('Indoor Temperature Over Time')
plt.legend()
plt.grid(True)

# Plot indoor and outdoor humidity
plt.subplot(4, 1, 3)
plt.plot(df['timestamp'], df['humidity'], label='Outdoor Humidity (%)', color='green')
plt.plot(df['timestamp'], df['indoor_humidity'], label='Indoor Humidity (%)', color='purple')
plt.xlabel('Timestamp')
plt.ylabel('Humidity (%)')
plt.title('Indoor and Outdoor Humidity Over Time')
plt.legend()
plt.grid(True)

# Plot solar radiation and UV index
plt.subplot(4, 1, 4)
plt.plot(df['timestamp'], df['solar_radiation'], label='Solar Radiation (W/m²)', color='gold')
plt.plot(df['timestamp'], df['uv_index'], label='UV Index', color='violet')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.title('Solar Radiation and UV Index Over Time')
plt.legend()
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
