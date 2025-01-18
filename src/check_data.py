from sqlalchemy import create_engine, text
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load import get_database_url

def check_data():
    """Check the collected weather data"""
    engine = create_engine(get_database_url())
    
    # Check current weather data
    print("\nLatest Weather Data:")
    query = """
    SELECT city, timestamp, temperature, humidity, description
    FROM weather_data
    WHERE timestamp >= NOW() - INTERVAL '1 hour'
    ORDER BY timestamp DESC;
    """
    df = pd.read_sql(query, engine)
    print(df)
    
    # Check daily aggregates
    print("\nDaily Aggregates (Last 24 hours):")
    query = """
    SELECT city, date, avg_temperature, min_temperature, max_temperature
    FROM weather_daily_aggregates
    WHERE date >= NOW() - INTERVAL '24 hours'
    ORDER BY date DESC;
    """
    df_agg = pd.read_sql(query, engine)
    print(df_agg)
    
    # Get row counts
    with engine.connect() as conn:
        weather_count = conn.execute(text("SELECT COUNT(*) FROM weather_data")).scalar()
        agg_count = conn.execute(text("SELECT COUNT(*) FROM weather_daily_aggregates")).scalar()
        
    print(f"\nTotal Records:")
    print(f"Weather Data: {weather_count} records")
    print(f"Daily Aggregates: {agg_count} records")

if __name__ == "__main__":
    check_data() 