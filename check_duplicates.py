import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Query the database for duplicate timestamps
query = '''
SELECT timestamp, COUNT(*) as count
FROM weather_data
GROUP BY timestamp
HAVING COUNT(*) > 1
'''

duplicates = pd.read_sql_query(query, conn)
print(duplicates)

# Close the database connection
conn.close()
