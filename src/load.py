from sqlalchemy import create_engine, Table, Column, Integer, Float, String, DateTime, MetaData
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import DB_CONFIG

def get_database_url():
    """Create database URL from config"""
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

def create_tables(engine):
    """Create database tables if they don't exist"""
    metadata = MetaData()
    
    # Weather data table
    Table('weather_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('city', String),
        Column('timestamp', DateTime),
        Column('temperature', Float),
        Column('feels_like', Float),
        Column('humidity', Integer),
        Column('pressure', Float),
        Column('wind_speed', Float),
        Column('wind_direction', Float),
        Column('wind_direction_cardinal', String),
        Column('description', String),
        Column('clouds', Integer),
        Column('temperature_celsius', Float),
        Column('data_timestamp', DateTime)
    )
    
    # Daily aggregations table
    Table('weather_daily_aggregates', metadata,
        Column('id', Integer, primary_key=True),
        Column('city', String),
        Column('date', DateTime),
        Column('avg_temperature', Float),
        Column('min_temperature', Float),
        Column('max_temperature', Float),
        Column('avg_humidity', Float),
        Column('avg_pressure', Float),
        Column('avg_wind_speed', Float)
    )
    
    metadata.create_all(engine)

def load_weather_data(df, engine):
    """
    Load weather data into the database
    """
    try:
        # Create tables if they don't exist
        create_tables(engine)
        
        # Load current weather data
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        
        return True
    except Exception as e:
        print(f"Error loading data to database: {str(e)}")
        return False

def load_daily_aggregates(daily_agg, engine):
    """
    Load daily aggregated data into the database
    """
    try:
        # Prepare the aggregated data
        daily_agg = daily_agg.reset_index()
        daily_agg.columns = ['city', 'date', 'avg_temperature', 'min_temperature', 
                           'max_temperature', 'avg_humidity', 'avg_pressure', 'avg_wind_speed']
        
        # Load to database
        daily_agg.to_sql('weather_daily_aggregates', engine, if_exists='append', index=False)
        
        return True
    except Exception as e:
        print(f"Error loading aggregated data to database: {str(e)}")
        return False

if __name__ == "__main__":
    # Test database connection
    try:
        engine = create_engine(get_database_url())
        create_tables(engine)
        print("Successfully connected to database and created tables.")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}") 