import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

# Station 2
# load in my API key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
url = "https://api.openweathermap.org/data/2.5/weather?"


# 6 famous cities 
cities = ["Dubai", "London", "Tokyo", "New York", "Cairo", "Paris"]

# Makes a GET request
all_cities_data = []
for city in cities:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Line used to look at what the API will return
    #print(json.dumps(data, indent=2))  
    
    #Parses the JSON response
    all_cities_data.append({
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_deg": data["wind"]["deg"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
        "country": data["sys"]["country"]
    })
    
    
# Stores relevant fields into a DataFrame
df = pd.DataFrame(all_cities_data)

# Print the first 5 rows of your DataFrame.
print(df.head(5))

# Add 3–5 lines of notes at the bottom of the script describing the data and possible uses.
# This dataset contains current weather data for 6 famous cities, pulled from the
# OpenWeatherMap API, including temperature, humidity, country that are in ,wind speed/direction, Coordinates (lat/lon) and
# general conditions (e.g. "clear sky").
# I could use this data to compare weather across cities in real time, track
# how conditions change if run periodically, or build a simple weather dashboard.