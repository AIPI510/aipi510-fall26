import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

#Create the API endpoint URL
url = "https://api.openweathermap.org/data/2.5/forecast"

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

#create an empty list to store the parsed data
rows = []

for item in data["list"]:
    rows.append({
        "city_name": data["city"]["name"],
        "date_time": item["dt_txt"],
        "description": item["weather"][0]["description"],
        "humidity": item["main"]["humidity"],
        "maximum_temp": item["main"]["temp_max"],
        "minimum_temp": item["main"]["temp_min"],
        "feels_like": item["main"]["feels_like"],
    })
 
#Convert to pandas DataFrame
df = pd.DataFrame(rows)
print(df.head())

#This data shows the weather data for New York City, including the city name, date and time of the forecast, weather description, humidity, maximum and minimum temperatures, and the "feels like" temperature. 
#The mean and median for columns humidity, maximum temperature, minimum temperature, and feels like temperature are all very similar, indicating that the data is relatively consistent and there are no extreme outliers and that the features are largely redundant. Please note that the code itself does not return the mean or median, but it was calculated separately. If curious, user can calculate the mean and median using df.mean() and df.median() respectively.
#This data can be used to analyze weather patterns in New York City and make predictions about future weather conditions. It can also help understand how volatile the weather is throughout the day and how it may affect daily activities.
