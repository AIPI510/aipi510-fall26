import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"
    }
    response = requests.get(url, params=params)
    data = response.json()

    return data

#####################################################################
#                          MAIN FUNCTION                            #
#####################################################################


city = ['Dallas', 'Durham', 'Los Angeles', 'Chicago', 'Raleigh', 'New York City']
temp = []
description = []

for c in city:
    data = get_weather(c)
    temp_data = data["main"]["temp"]
    temp.append(temp_data)
    description_data = data["weather"][0]["description"]
    description.append(description_data)

df = pd.DataFrame({
    'city': city,
    'temperature': temp,
    'weather': description
})

print(df)

# Plotting temperatures
plt.figure()
plt.scatter(df['city'], df['temperature'])
plt.title("City versus temperature")
plt.xlabel("City")
plt.ylabel("Temperature")
plt.show()


# This code can be used to find and compare weather at different locations.
# It currently uses a preset list of cities but the list can be changed and can also be used to solicit user input instead.
# The code will then plot the different temperatures to compare them against each other based on city.