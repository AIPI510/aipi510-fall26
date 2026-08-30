import datetime as dt
import json
import numpy as np
import os
import pandas as pd
import random
import requests

from dotenv import load_dotenv

OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Load user's open weather configuration
load_dotenv()
OPEN_WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Set random generator seed, for reproducibility
# TODO: Comment or remove for practical use
random.seed(62)

# Collect weather data for 50 US-ish locations
records = []
for i in range(50):
    # Query OpenWeatherMap for current weather data
    params = {
        "lat": random.uniform(24.5, 49.5), # approximate US lat boundaries
        "lon": random.uniform(-124.8, -66.9), # approximate US lon boundaries
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial"
    }
    data = requests.get(OPEN_WEATHER_URL, params=params).json()

    # Calculate and format time according to local timezone
    local_tz = dt.timezone(dt.timedelta(seconds=data["timezone"]))
    local_time = dt.datetime.fromtimestamp(data["dt"], tz=local_tz)
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

    # Select identify info (city name, lat, lon) and measurement-like fields
    weather_data = {}
    weather_data['city'] = data['name'].strip()
    weather_data['local_time'] = formatted_time
    weather_data = weather_data | data['coord']
    weather_data = weather_data | data['main']
    weather_data = weather_data | {
        'wind_speed': data['wind']['speed'],
        'wind_deg': data['wind']['deg'],
        'cloudiness_percentage': data['clouds']['all']
    }

    # Append weather data
    records.append(weather_data)

# Construct dataframe
df = pd.DataFrame(records)

# Drop row entries that OpenWeatherMap was not able to label with a city name
df = df[~(df['city'] == "")]

# Rename columns for clarity
df = df.rename(
    columns={
        "humidity": "humidity_percentage", 
        "pressure": "sea_level_pressure_hPa"
    }
)

# Drop additional pressure fields
df.drop(columns=['sea_level', 'grnd_level'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Display the first five entries of dataframe
print(df.head())

# ============================================================================
# The data in this dataframe describes the weather in a number of 
# pseudo-random locations across the US or US-adjacent countries. Row entries 
# represent individual city temperature recordings; columns describe recording 
# details (lat, long coordinates, local time the recording was taken, name of 
# city) and weather statistics. Temperatures are listed in degrees Fahrenheit, 
# speeds in miles per hour, other quantity units are documented in column 
# names. If used to generate a greater quantity of data, this script could be 
# used in conjunction with other datasets to examine the effect of weather on 
# other phenomena (like traffic, sports performance, communications 
# reliability).
