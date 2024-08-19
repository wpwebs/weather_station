#! .weather_station/bin/python

import sqlite3
import pandas as pd
from windrose import WindroseAxes
import matplotlib.pyplot as plt
import sys

# Accept an argument for including or excluding indoor temperature
indoor = sys.argv[1] if len(sys.argv) > 1 else 'yes'

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query data from the database
query = '''
SELECT timestamp, wind_speed, wind_direction, temperature, indoor_temperature
FROM weather_data
'''
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Clean up the data
# Remove duplicate entries
df = df.drop_duplicates(subset=['timestamp', 'wind_speed', 'wind_direction', 'temperature', 'indoor_temperature'])

# Remove rows with missing data
df = df.dropna(subset=['timestamp', 'wind_speed', 'wind_direction', 'temperature'])

# If indoor_temperature is included, ensure it's cleaned up as well
if indoor.lower() != 'no':
    df = df.dropna(subset=['indoor_temperature'])

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

# Create the wind rose chart with temperature overlay
def create_wind_rose_with_temps(ax, dataframe, title, include_indoor):
    windrose_ax = WindroseAxes.from_ax(ax=ax)
    windrose_ax.bar(dataframe['wind_direction'], dataframe['wind_speed'], normed=True, opening=0.8, edgecolor='white')
    
    # Overlay outdoor temperature as scatter plot
    scatter_outdoor = windrose_ax.scatter(
        dataframe['wind_direction'], dataframe['wind_speed'], 
        c=dataframe['temperature'], cmap='coolwarm', 
        alpha=0.7, edgecolor='k', label='Outdoor Temp'
    )

    # Overlay indoor temperature as scatter plot with different marker, if included
    if include_indoor:
        scatter_indoor = windrose_ax.scatter(
            dataframe['wind_direction'], dataframe['wind_speed'], 
            c=dataframe['indoor_temperature'], cmap='viridis', 
            alpha=0.7, marker='x', label='Indoor Temp'
        )
    
    windrose_ax.set_legend()
    ax.set_title(title)
    
    # Add color bars for temperature
    cbar_outdoor = plt.colorbar(scatter_outdoor, ax=ax, label='Outdoor Temperature (°C)')
    
    if include_indoor:
        cbar_indoor = plt.colorbar(scatter_indoor, ax=ax, label='Indoor Temperature (°C)')

# Set up a 2x2 grid for the plots
fig, axes = plt.subplots(2, 2, figsize=(14, 12), subplot_kw={'projection': 'windrose'})
fig.suptitle('Wind Rose Charts with Temperature Overlay for Different Time Periods')

# Generate the wind rose charts with or without indoor temperature for each time period
include_indoor = indoor.lower() != 'no'
for ax, (period, (start_hour, end_hour)) in zip(axes.flatten(), time_periods.items()):
    if period != 'All Time':
        period_df = df[(df['hour'] >= start_hour) & (df['hour'] < end_hour)]
    else:
        period_df = df
    
    create_wind_rose_with_temps(ax, period_df, f'{period}', include_indoor)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the plots and block the script from exiting
plt.show(block=True)
