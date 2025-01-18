from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Cities to monitor (add or modify as needed)
CITIES = [
    "London,UK",
    "New York,US",
    "Tokyo,JP",
    "Paris,FR",
    "Sydney,AU",
    "Kuala Lumpur,MY"
]

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'weather_data'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')
}

# Data collection frequency (in minutes)
UPDATE_FREQUENCY = 30

# Units (metric/imperial)
UNITS = "metric" 