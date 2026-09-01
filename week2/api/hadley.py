import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key 
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "units": "imperial",
        "appid": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    weather_info = {
        "city": data["name"],
        "temperature_F": data["main"]["temp"],
        "feels_like_F": data["main"]["feels_like"],
        "humidity_pct": data["main"]["humidity"],
        "conditions": data["weather"][0]["description"],
        "wind_speed_mph": data["wind"]["speed"]
    }

    df = pd.DataFrame([weather_info])
    print(df)
    return df

city = input("Enter a city:")
get_weather(city)

# Notes:
# This python script retrieves current weather data from a city that is inputted by the user. It gets this data
# from the OpenWeatherMap API and returns it as a JSON. The data includes information like temperature, humidity, 
# wind, and more. Some possible uses for this include just simply getting live weather data or you could use it to 
# build a simple weather-checking app. 