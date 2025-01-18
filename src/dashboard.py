import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load import get_database_url

# Page config
st.set_page_config(
    page_title="Weather Data Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Title and description
st.title("🌤️ Weather Data Dashboard")
st.markdown("Real-time weather data from multiple cities around the world")

# Initialize database connection
@st.cache_resource
def init_connection():
    return create_engine(get_database_url())

# Fetch data with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data():
    engine = init_connection()
    
    # Get latest weather data
    query = """
    SELECT city, timestamp, temperature, humidity, pressure, 
           wind_speed, description, clouds
    FROM weather_data
    WHERE timestamp >= NOW() - INTERVAL '24 hours'
    ORDER BY timestamp DESC;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def get_daily_aggregates():
    engine = init_connection()
    query = """
    SELECT city, date, avg_temperature, min_temperature, max_temperature,
           avg_humidity, avg_pressure, avg_wind_speed
    FROM weather_daily_aggregates
    WHERE date >= NOW() - INTERVAL '7 days'
    ORDER BY date DESC;
    """
    return pd.read_sql(query, engine)

# Load data
df = get_weather_data()
df_agg = get_daily_aggregates()

# Current Weather Section
st.header("Current Weather Conditions")

# Create columns for current weather cards
cities = df['city'].unique()
cols = st.columns(len(cities))

for idx, city in enumerate(cities):
    latest_data = df[df['city'] == city].iloc[0]
    with cols[idx]:
        st.metric(
            label=city,
            value=f"{latest_data['temperature']:.1f}°C",
            delta=f"Humidity: {latest_data['humidity']}%"
        )
        st.caption(f"Description: {latest_data['description'].title()}")

# Weather Insights Section
st.header("Weather Insights")

# Weather Pattern Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Weather Pattern Distribution")
    # Group and count weather descriptions
    weather_patterns = df.groupby(['city', 'description']).size().reset_index(name='count')
    fig_patterns = px.treemap(
        weather_patterns,
        path=[px.Constant("All Cities"), 'city', 'description'],
        values='count',
        title='Weather Patterns by City',
        color='count',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_patterns, use_container_width=True)

with col2:
    st.subheader("Temperature vs. Pressure Correlation")
    fig_correlation = px.scatter(
        df,
        x='temperature',
        y='pressure',
        color='city',
        title='Temperature vs. Pressure Relationship',
        labels={
            'temperature': 'Temperature (°C)',
            'pressure': 'Pressure (hPa)'
        },
        trendline="ols"  # Add trend lines
    )
    st.plotly_chart(fig_correlation, use_container_width=True)

# Weather Metrics
col1, col2 = st.columns(2)

with col1:
    st.subheader("Wind Speed by City")
    fig_wind = px.bar(
        df.groupby('city')['wind_speed'].mean().reset_index(),
        x='city',
        y='wind_speed',
        title='Average Wind Speed',
        labels={'wind_speed': 'Wind Speed (m/s)'}
    )
    st.plotly_chart(fig_wind, use_container_width=True)

with col2:
    st.subheader("Humidity Levels")
    fig_humidity = px.box(
        df,
        x='city',
        y='humidity',
        title='Humidity Distribution',
        labels={'humidity': 'Humidity (%)'}
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

# Add weather summary statistics
st.header("Weather Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp = df.groupby('city')['temperature'].mean().round(1)
    st.metric("Average Temperature", f"{avg_temp.mean():.1f}°C",
              delta=f"Range: {avg_temp.min():.1f}°C to {avg_temp.max():.1f}°C")

with col2:
    cloud_coverage = df['clouds'].mean().round(1)
    st.metric("Average Cloud Coverage", f"{cloud_coverage:.1f}%",
              delta=f"Based on {len(df)} measurements")

with col3:
    pressure_avg = df['pressure'].mean().round(1)
    st.metric("Average Pressure", f"{pressure_avg:.1f} hPa",
              delta=f"Std: {df['pressure'].std():.1f} hPa")

# Detailed Data Table
st.header("Recent Weather Data")
st.dataframe(
    df[['city', 'timestamp', 'temperature', 'humidity', 'wind_speed', 'description']]
    .sort_values('timestamp', ascending=False)
    .head(10)
) 