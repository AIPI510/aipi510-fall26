import requests
import json
import pandas as pd

API_KEY = "YOUR_API_KEY_HERE"
CITY = "Durham"

url = "https://api.openweathermap.org/data/2.5/weather"
params = {"q": CITY, "appid": API_KEY, "units": "imperial"}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame([{
    "city": data["name"],
    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather": data["weather"][0]["description"]
}])

print(df.head())

# --- Notes ---
# This is current weather data for one city from OpenWeatherMap.
# Could be used to track weather over time or compare across cities.
# Limitation: only shows current conditions, no historical data.