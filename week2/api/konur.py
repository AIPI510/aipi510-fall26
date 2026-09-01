import requests
import json
import pandas as pd

# USGS feed containing earthquakes of magnitude 2.5+ from the past day
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

# Pull from the API
response = requests.get(url, timeout=10)
response.raise_for_status()
data = json.loads(response.text)

# Want magnitude, location, time
# longitude, latitude, and depth of the earthquake
earthquakes = []

for feature in data["features"]:
    properties = feature["properties"]
    coordinates = feature["geometry"]["coordinates"]

    earthquake = {
        "magnitude": properties["mag"],
        "location": properties["place"],
        "time": properties["time"],
        "longitude": coordinates[0],
        "latitude": coordinates[1],
        "depth_km": coordinates[2]
    }

    earthquakes.append(earthquake)


df = pd.DataFrame(earthquakes)
df["time"] = pd.to_datetime(df["time"], unit="ms")

# Clean up the data
df = df.dropna()
df = df.reset_index(drop=True)

# Print first five rows
print(df.head())

# This data shows the most recent earthquakes of magnitude 2.5 
# over the past day. It tells us magnitude, location, data and time, 
# depth of the earthquake. We can use this data to keep up-to-date on
# current earthquakes around the world, and to add new data every day to 
# a training set for an earthquake model. 