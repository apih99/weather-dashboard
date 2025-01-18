import requests
import pandas as pd
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    OPENWEATHERMAP_API_KEY,
    BASE_URL,
    CITIES,
    UNITS
)

def fetch_weather_data():
    """
    Fetch weather data for configured cities from OpenWeatherMap API
    Returns a pandas DataFrame with the weather data
    """
    weather_data = []
    
    for city in CITIES:
        try:
            params = {
                'q': city,
                'appid': OPENWEATHERMAP_API_KEY,
                'units': UNITS
            }
            
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information
            weather_info = {
                'city': city,
                'timestamp': datetime.utcfromtimestamp(data['dt']),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', None),
                'description': data['weather'][0]['description'],
                'clouds': data['clouds']['all']
            }
            
            weather_data.append(weather_info)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {str(e)}")
            continue
    
    return pd.DataFrame(weather_data)

if __name__ == "__main__":
    # Test the extraction
    df = fetch_weather_data()
    print(df.head()) 