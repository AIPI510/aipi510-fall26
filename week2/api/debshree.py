import pandas as pd
import requests

# 1. Make a GET request to the Open-Meteo public Weather API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.7128,   # Example: New York City
    "longitude": -74.0060,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

response = requests.get(url, params=params)

# Ensure the request was successful
response.raise_for_status()

# 2. Parse the JSON response
data = response.json()

# 3. Store relevant hourly fields into a DataFrame
hourly_data = data.get("hourly", {})

df = pd.DataFrame({
    "Time": hourly_data.get("time"),
    "Temperature_C": hourly_data.get("temperature_2m"),
    "Humidity_%": hourly_data.get("relative_humidity_2m"),
    "WindSpeed_kmh": hourly_data.get("wind_speed_10m")
})

# 4. Print the first 5 rows
print(df.head())

'''This code helps to get data from open source weather API and to load it in a table format for analysis'''