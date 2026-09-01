import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 1. Create the API endpoint URL
url = "https://api.openweathermap.org/data/2.5/forecast"

# 2. Set query parameters
city = "Durham"
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"  # temperature in Celsius
}

# 3. Make the request
response = requests.get(url, params=params)

# 4. Parse JSON
data = response.json()


df = pd.json_normalize(data, 'list')
print(df.head(5))

'''
The dataframe holds the weather forecast in 3 hour intervals for the next 5 days for a given city (I chose Durham).
There's a variety of weather data that could be used to nicely display to people so they can prepare for the weather in the upcoming week.
Meteorologists or other scientists could use this data to analyze the predictions given vs. the actual weather when it does come in order to see how prediction can be improved.
'''