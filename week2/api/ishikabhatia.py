import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY is None)

#Create the API endpoint URL
url = "https://api.openweathermap.org/data/2.5/weather"

#Set query parameters
city = "New York"
params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # temperature in Celsius
    }

#Make the request
response = requests.get(url, params=params)
    
#Parse JSON
data = response.json()

parsed_data = {
    "city_name": data["name"],
    "temp": data["main"]["temp"],
    "description": data["weather"][0]["description"],
    "humidity": data["main"]["humidity"],
    "maximum_temp": data["main"]["temp_max"],
    "minimum_temp": data["main"]["temp_min"],
    "feels_like": data["main"]["feels_like"]
}

#Convert to pandas DataFrame
df = pd.DataFrame([parsed_data])
print(df.head())