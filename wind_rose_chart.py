#! .weather_station/bin/python

import sqlite3
import pandas as pd
from windrose import WindroseAxes
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query data from the database
query = '''
SELECT timestamp, wind_speed, wind_direction 
FROM weather_data
'''
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Clean up the data
# Remove duplicate entries
df = df.drop_duplicates(subset=['timestamp', 'wind_speed', 'wind_direction'])

# Remove rows with missing data
df = df.dropna(subset=['timestamp', 'wind_speed', 'wind_direction'])

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract hour from timestamp
df['hour'] = df['timestamp'].dt.hour

# Define time periods
time_periods = {
    'Before Noon': (0, 12),
    'After Noon': (12, 18),
    'Night': (18, 24),
    'All Time': (0, 24)
}

# Create the wind rose chart
def create_wind_rose(ax, dataframe, title):
    windrose_ax = WindroseAxes.from_ax(ax=ax)
    windrose_ax.bar(dataframe['wind_direction'], dataframe['wind_speed'], normed=True, opening=0.8, edgecolor='white')
    windrose_ax.set_legend()
    ax.set_title(title)

# Set up a 2x2 grid for the plots
fig, axes = plt.subplots(2, 2, figsize=(14, 12), subplot_kw={'projection': 'windrose'})
fig.suptitle('Wind Rose Charts for Different Time Periods')

# Generate the wind rose charts for each time period
for ax, (period, (start_hour, end_hour)) in zip(axes.flatten(), time_periods.items()):
    if period != 'All Time':
        period_df = df[(df['hour'] >= start_hour) & (df['hour'] < end_hour)]
    else:
        period_df = df
    
    create_wind_rose(ax, period_df, f'{period}')

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the plots and block the script from exiting
plt.show(block=True)
