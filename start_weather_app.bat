@echo off
echo Starting Weather Data ETL Pipeline...

REM Start the ETL pipeline in a new window
start cmd /k ".\venv\Scripts\activate && python src/etl_pipeline.py"

REM Wait for a moment to ensure the ETL pipeline has started
timeout /t 5

REM Start the dashboard
echo Starting Dashboard...
start cmd /k ".\venv\Scripts\activate && streamlit run src/dashboard.py" 