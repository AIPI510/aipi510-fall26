import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

cities = ["Durham", "New York", "Chicago", "Denver", "Seattle"]

url = "https://api.openweathermap.org/data/2.5/weather"

records = []
for city in cities:
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial",  # or "metric" for Celsius
    }

    response = requests.get(url, params=params)
    print(city, response.status_code)  # 200 = success, 401 = bad/inactive key
    data = response.json()  # parses the JSON response body into a Python dict

    #flatten the nested JSON structure into a single-level dict for easier DataFrame creation
    record = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }
    records.append(record)

df = pd.DataFrame(records)  # one row per city

print(df.head())

# Notes:
# - Data source: OpenWeatherMap's "Current Weather" API, one call per city, for 5
#   US cities (Durham, New York, Chicago, Denver, Seattle).
# - Each row is a snapshot of current conditions for one city at the moment the
#   script ran: temperature, feels-like temperature, humidity, pressure, a short
#   text description (e.g. "clear sky"), and wind speed (imperial units).
# - Because it's a live snapshot, re-running the script later will give different
#   values - this isn't a static/historical dataset unless you save each run's
#   output somewhere (e.g. append to a CSV on a schedule).
# - Possible uses: track weather across cities over time by running this on a
#   schedule and appending results, compare conditions across cities on a given
#   day, or join against other per-city datasets (e.g. population) by city name.
