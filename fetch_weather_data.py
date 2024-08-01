import requests
import time
from datetime import datetime, timedelta
import sqlite3
from datetime import datetime

# Replace with your actual API key and Application Key
API_KEY = 'ba96647de7e4446b80a79351838ca2dce29ab6bd8b91413d9df101b54d398899'
APP_KEY = 'c8a3bd5a81914fb3add65af391d59445042b59be7e5848d5a46f90e4f9eba654'
STATION_ID = '48:55:19:C2:81:F9'
API_URL = f'https://api.ambientweather.net/v1/devices/{STATION_ID}?apiKey={API_KEY}&applicationKey={APP_KEY}'

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

def fetch_latest_timestamp():
    cursor.execute('SELECT last_update FROM latest_timestamp WHERE id = 1')
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return '2024-07-27 00:00:00'  # Use a more recent default timestamp

def update_latest_timestamp(new_timestamp):
    cursor.execute('UPDATE latest_timestamp SET last_update = ? WHERE id = 1', (new_timestamp,))
    conn.commit()

def fetch_weather_data(end_date):
    url = f'{API_URL}&limit=288&endDate={end_date}'
    print(f"Fetching URL: {url}")  # Debugging: Print the URL being fetched
    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")  # Debugging: Print the response status code
        print(f"Response Text: {response.text}")  # Debugging: Print the raw response text
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"General error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    return []

def process_weather_data(data):
    processed_data = []
    for entry in data:
        if 'dateutc' in entry:  # Check if key exists to avoid KeyError
            timestamp = datetime.utcfromtimestamp(entry['dateutc'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            processed_data.append((
                timestamp,
                entry.get('tempf'),
                entry.get('humidity'),
                entry.get('windspeedmph'),
                entry.get('winddir'),
                entry.get('solarradiation', None),  # Solar Radiation
                entry.get('uv', None),  # UV Index
                entry.get('tempinf', None),  # Indoor Temperature
                entry.get('humidityin', None),  # Indoor Humidity
                entry.get('feelsLike', None)  # Outdoor Feels Like
            ))
    return processed_data

def save_to_db(data):
    cursor.executemany('''INSERT INTO weather_data (timestamp, temperature, humidity, wind_speed, wind_direction, solar_radiation, uv_index, indoor_temperature, indoor_humidity, outdoor_feels_like)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()

def main():
    last_update = fetch_latest_timestamp()
    last_update_dt = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.utcnow()

    empty_response_count = 0
    max_empty_responses = 5  # Allow up to 5 consecutive empty responses before breaking the loop

    while last_update_dt < current_time:
        next_day = last_update_dt + timedelta(days=1)
        end_date = next_day.strftime('%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 format with UTC 'Z'

        print(f"Fetching data up to {end_date}")
        data = fetch_weather_data(end_date)
        if not data:
            print("No data fetched for this date range.")
            empty_response_count += 1
            if empty_response_count >= max_empty_responses:
                print("No more data to fetch. Exceeded max empty responses.")
                break
        else:
            empty_response_count = 0
            weather_data = process_weather_data(data)
            if weather_data:  # Check if there's any processed data
                save_to_db(weather_data)
                print(f"Processed and saved {len(weather_data)} records.")
                # Update the latest timestamp to the end of the current batch
                last_timestamp = max(entry[0] for entry in weather_data)
                last_update_dt = datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S')
                last_update = last_update_dt.strftime('%Y-%m-%d %H:%M:%S')
                update_latest_timestamp(last_update)
            else:
                print("No new data to process.")
        last_update_dt = next_day  # Move to the next day regardless of data fetched
        last_update = next_day.strftime('%Y-%m-%d %H:%M:%S')
        update_latest_timestamp(last_update)
        # Sleep to avoid hitting API rate limits
        time.sleep(1)

if __name__ == '__main__':
    main()

# Close the database connection
conn.close()