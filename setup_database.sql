-- Create the database
CREATE DATABASE weather_data;

-- Connect to the database
\c weather_data;

-- Create a new user (if you want a different user than postgres)
-- Uncomment and modify these lines if you want a separate user
-- CREATE USER weather_user WITH PASSWORD 'your_password_here';
-- GRANT ALL PRIVILEGES ON DATABASE weather_data TO weather_user;

-- The tables will be created automatically by the Python application
-- when it runs for the first time 