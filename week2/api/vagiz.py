"""You can specify the city to get the weather conditions for."""


import requests

import json

import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    """
    Fetch weather for the given city and print it nicely.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # temperature in Celsius
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


if __name__ == "__main__":
    response = get_weather("Durham")

    df = pd.DataFrame(response.json()["main"], index=[0])
    print(df)

