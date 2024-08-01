import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query data from the database
query = '''
SELECT timestamp, solar_radiation, uv_index
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
plt.figure(figsize=(15, 10))

# Plot solar radiation
plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['solar_radiation'], label='Solar Radiation (W/m²)', color='gold')
plt.xlabel('Timestamp')
plt.ylabel('Solar Radiation (W/m²)')
plt.title('Solar Radiation Over Time')
plt.legend()
plt.grid(True)

# Plot UV index
plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['uv_index'], label='UV Index', color='violet')
plt.xlabel('Timestamp')
plt.ylabel('UV Index')
plt.title('UV Index Over Time')
plt.legend()
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
