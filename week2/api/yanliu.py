import json
import pandas as pd
import requests

API_KEY = "aa4443183d95f6c569e65a5db8b47e22"
city = "Durham"
url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q":city,
    "appid":API_KEY,
    "units":"metric"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    weather_data = {
        "City": data["name"],
        "Temperature (°C)": data["main"]["temp"],
        "Weather": data["weather"][0]["description"],
        "Humidity (%)": data["main"]["humidity"],
        "Wind Speed (m/s)": data["wind"]["speed"]
    }
    df = pd.DataFrame([weather_data])
    print(df.head())

# This dataset contains current weather information for Durham, including temperature, humidity, weather conditions, and wind speed.
# The data could be used to build a weather monitoring tool.
# It could also be combined with data from multiple cities to compare weather patterns.