import requests
import json
import pandas as pd


# Open-Meteo forecast API
url = "https://api.open-meteo.com/v1/forecast"

# Durham, North Carolina
params = {
    "latitude": 35.9940,
    "longitude": -78.8986,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "precipitation_probability_max"
    ],
    "temperature_unit": "fahrenheit",
    "forecast_days": 5,
    "timezone": "America/New_York"
}


# Make GET request
response = requests.get(url, params=params)

# Check for request errors
response.raise_for_status()

# Parse JSON response
data = response.json()


# Store relevant fields in a DataFrame
df = pd.DataFrame({
    "date": data["daily"]["time"],
    "high_temp_f": data["daily"]["temperature_2m_max"],
    "low_temp_f": data["daily"]["temperature_2m_min"],
    "feels_like_high_f": data["daily"]["apparent_temperature_max"],
    "rain_probability_percent": data["daily"]["precipitation_probability_max"]
})


# Print first 5 rows
print("Durham 5-Day Weather Forecast:")
print(df.head())


# Notes:
# This dataset contains a five-day weather forecast for Durham, North Carolina.
# It includes daily high and low temperatures, maximum feels-like temperature,
# and maximum precipitation probability.
# The data can be used to examine heatwave conditions and compare expected heat across days.