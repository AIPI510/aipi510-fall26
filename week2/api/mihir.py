import requests
import json
import pandas as pd

API_KEY = "YOUR_API_KEY_HERE"
CITIES = ["Durham", "New York", "Los Angeles", "Chicago", "Miami"]

url = "https://api.openweathermap.org/data/2.5/weather"

records = []
for city in CITIES:
    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    response = requests.get(url, params=params)
    data = response.json()
    records.append({
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    })

df = pd.DataFrame(records)
print(df.head())

# --- Notes ---
# This is current weather data for 5 cities from OpenWeatherMap.
# Could be used to track weather over time or compare across cities.
# Limitation: only shows current conditions, no historical data.