# Weather Data ETL Pipeline with Real-time Dashboard

A comprehensive data engineering project that collects, processes, and visualizes weather data from multiple cities worldwide using OpenWeatherMap API. The project demonstrates ETL (Extract, Transform, Load) pipeline implementation with real-time data visualization.

![Project Type](https://img.shields.io/badge/Project-Data%20Engineering-blue)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### ETL Pipeline
- **Extract**: Fetches real-time weather data from OpenWeatherMap API
- **Transform**: Cleans and processes data, including:
  - Temperature and pressure normalization
  - Wind direction conversion to cardinal points
  - Data aggregation for daily statistics
- **Load**: Stores data in PostgreSQL database with:
  - Real-time weather conditions table
  - Daily aggregated statistics table

### Interactive Dashboard
- **Current Conditions**: Real-time weather metrics for each city
- **Weather Insights**:
  - Weather pattern distribution visualization
  - Temperature vs. Pressure correlation analysis
- **Weather Metrics**:
  - Wind speed analysis
  - Humidity distribution
- **Summary Statistics**:
  - Average temperature ranges
  - Cloud coverage metrics
  - Pressure statistics

## 🏗️ Project Structure
```
weatherDataEngineering/
├── config/
│   └── config.py          # Configuration settings
├── src/
│   ├── extract.py         # Data extraction module
│   ├── transform.py       # Data transformation module
│   ├── load.py           # Database operations
│   ├── etl_pipeline.py   # Main ETL orchestration
│   ├── check_data.py     # Data validation utility
│   └── dashboard.py      # Streamlit dashboard
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── start_weather_app.bat # Startup script
└── README.md            # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- OpenWeatherMap API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weatherDataEngineering
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your:
- OpenWeatherMap API key
- PostgreSQL credentials

5. Start the application:
```bash
# Option 1: Using batch script (Windows)
.\start_weather_app.bat

# Option 2: Manual start
# Terminal 1 - ETL Pipeline
python src/etl_pipeline.py

# Terminal 2 - Dashboard
streamlit run src/dashboard.py
```

## 🔧 Configuration

### Adding/Modifying Cities
Edit `config/config.py`:
```python
CITIES = [
    "London,UK",
    "New York,US",
    "Tokyo,JP",
    # Add more cities
]
```

### Update Frequency
Modify in `config/config.py`:
```python
UPDATE_FREQUENCY = 30  # minutes
```

### Temperature Units
Choose between metric/imperial in `config/config.py`:
```python
UNITS = "metric"  # or "imperial"
```

## 📊 Dashboard Features

### Current Weather Conditions
- Real-time temperature
- Humidity levels
- Weather descriptions

### Weather Insights
- **Weather Pattern Distribution**: Treemap visualization showing weather patterns across cities
- **Temperature-Pressure Correlation**: Scatter plot with trend lines showing relationship between temperature and pressure

### Weather Metrics
- **Wind Speed Analysis**: Average wind speed by city
- **Humidity Distribution**: Box plot showing humidity patterns

### Summary Statistics
- Average temperatures with ranges
- Cloud coverage statistics
- Pressure metrics with standard deviation

## 🗄️ Database Schema

### weather_data
- id (Primary Key)
- city
- timestamp
- temperature
- feels_like
- humidity
- pressure
- wind_speed
- wind_direction
- wind_direction_cardinal
- description
- clouds
- temperature_celsius
- data_timestamp

### weather_daily_aggregates
- id (Primary Key)
- city
- date
- avg_temperature
- min_temperature
- max_temperature
- avg_humidity
- avg_pressure
- avg_wind_speed

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. Make sure to:
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests if applicable
5. Update documentation as needed

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- OpenWeatherMap API for weather data
- Streamlit for the dashboard framework
- Plotly for interactive visualizations 