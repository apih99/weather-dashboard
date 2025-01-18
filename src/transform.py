import pandas as pd
import numpy as np

def clean_weather_data(df):
    """
    Clean and transform the weather data
    """
    # Create a copy to avoid modifying the original dataframe
    df_clean = df.copy()
    
    # Convert wind direction to cardinal directions
    def degrees_to_cardinal(degrees):
        if pd.isna(degrees):
            return None
        
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / (360 / len(directions))) % len(directions)
        return directions[index]
    
    df_clean['wind_direction_cardinal'] = df_clean['wind_direction'].apply(degrees_to_cardinal)
    
    # Round numerical values
    numeric_columns = ['temperature', 'feels_like', 'wind_speed', 'pressure']
    df_clean[numeric_columns] = df_clean[numeric_columns].round(2)
    
    # Ensure humidity and clouds are integers
    df_clean['humidity'] = df_clean['humidity'].astype(int)
    df_clean['clouds'] = df_clean['clouds'].astype(int)
    
    # Convert description to lowercase for consistency
    df_clean['description'] = df_clean['description'].str.lower()
    
    # Add derived features
    df_clean['temperature_celsius'] = df_clean['temperature']  # Already in Celsius if UNITS='metric'
    df_clean['data_timestamp'] = pd.to_datetime('now', utc=True)
    
    return df_clean

def aggregate_weather_data(df):
    """
    Create aggregated views of the weather data
    """
    # Daily averages by city
    daily_agg = df.groupby(['city', pd.Grouper(key='timestamp', freq='D')]).agg({
        'temperature': ['mean', 'min', 'max'],
        'humidity': 'mean',
        'pressure': 'mean',
        'wind_speed': 'mean'
    }).round(2)
    
    return daily_agg

if __name__ == "__main__":
    # Test with sample data
    sample_data = pd.DataFrame({
        'city': ['London,UK'],
        'timestamp': [pd.Timestamp.now()],
        'temperature': [20.5],
        'feels_like': [19.8],
        'humidity': [80],
        'pressure': [1013.25],
        'wind_speed': [5.7],
        'wind_direction': [180],
        'description': ['Partly Cloudy'],
        'clouds': [75]
    })
    
    cleaned_data = clean_weather_data(sample_data)
    print("\nCleaned Data:")
    print(cleaned_data) 