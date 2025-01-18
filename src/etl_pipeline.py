import schedule
import time
from sqlalchemy import create_engine
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract import fetch_weather_data
from transform import clean_weather_data, aggregate_weather_data
from load import get_database_url, load_weather_data, load_daily_aggregates
from config.config import UPDATE_FREQUENCY

def run_etl_pipeline():
    """
    Execute the complete ETL pipeline
    """
    try:
        print("\nStarting ETL pipeline...")
        
        # Extract
        print("Extracting weather data...")
        raw_data = fetch_weather_data()
        
        if raw_data.empty:
            print("No data extracted. Skipping remaining steps.")
            return
        
        # Transform
        print("Transforming weather data...")
        cleaned_data = clean_weather_data(raw_data)
        daily_aggregates = aggregate_weather_data(cleaned_data)
        
        # Load
        print("Loading data to database...")
        engine = create_engine(get_database_url())
        
        # Load current weather data
        if load_weather_data(cleaned_data, engine):
            print("Successfully loaded current weather data.")
        else:
            print("Failed to load current weather data.")
        
        # Load daily aggregates
        if load_daily_aggregates(daily_aggregates, engine):
            print("Successfully loaded daily aggregates.")
        else:
            print("Failed to load daily aggregates.")
        
        print("ETL pipeline completed successfully.\n")
        
    except Exception as e:
        print(f"Error in ETL pipeline: {str(e)}")

def main():
    """
    Main function to run the ETL pipeline on a schedule
    """
    print(f"Weather Data ETL Pipeline")
    print(f"Scheduled to run every {UPDATE_FREQUENCY} minutes")
    
    # Run once immediately
    run_etl_pipeline()
    
    # Schedule regular runs
    schedule.every(UPDATE_FREQUENCY).minutes.do(run_etl_pipeline)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 