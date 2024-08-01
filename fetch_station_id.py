import requests

# Replace with your actual API key and Application Key
API_KEY = 'ba96647de7e4446b80a79351838ca2dce29ab6bd8b91413d9df101b54d398899'
APP_KEY = 'c8a3bd5a81914fb3add65af391d59445042b59be7e5848d5a46f90e4f9eba654'
API_URL = f'https://api.ambientweather.net/v1/devices?apiKey={API_KEY}&applicationKey={APP_KEY}'

def fetch_station_details():
    response = requests.get(API_URL)
    data = response.json()
    return data

def main():
    stations = fetch_station_details()
    for station in stations:
        print(f"Station Name: {station['info']['name']}")
        print(f"Station ID: {station['macAddress']}")

if __name__ == '__main__':
    main()
