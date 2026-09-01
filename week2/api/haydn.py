import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")

response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": "London,uk", "appid": OWM_API_KEY}
)

weather_df = pd.DataFrame([response.json()])

weather_df.to_csv("week2/api/haydn_weather.csv", index=False)

for i in range(5):
    print(weather_df.iloc[i])  # print the first 5 lines (Step 7)

'''
The data I'm collecting specifically is the current weather data for London. I could use this data, for any city (or cities), in the
world to track weather patterns over time. I could also display that data on a screen in my home, office, or a public space.
Another possible use is to estimate solar power generation for a region.
'''
