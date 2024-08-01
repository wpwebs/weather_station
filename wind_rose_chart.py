import sqlite3
import pandas as pd
from windrose import WindroseAxes
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query data from the database
query = '''SELECT wind_speed, wind_direction FROM weather_data'''
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Clean up the data
# Remove duplicate entries
df = df.drop_duplicates(subset=['wind_speed', 'wind_direction'])

# Remove rows with missing wind speed or direction
df = df.dropna(subset=['wind_speed', 'wind_direction'])

# Create the wind rose chart
def create_wind_rose(dataframe):
    ax = WindroseAxes.from_ax()
    ax.bar(dataframe['wind_direction'], dataframe['wind_speed'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    plt.title('Wind Rose')
    plt.show()

# Generate the wind rose chart
create_wind_rose(df)
