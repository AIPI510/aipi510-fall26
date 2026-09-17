import requests
import json
import pandas as pd

# select api
url = "https://v2.jokeapi.dev/joke/Any?amount=10"

# make a get request
response = requests.get(url)

# parse response
data = response.json()

# store fields
jokes = []

for joke in data["jokes"]:
    jokes.append({
        "category": joke["category"],
        "type": joke["type"],
        "joke": joke.get("joke", joke.get("setup", "")),
        "delivery": joke.get("delivery", "")
    })

# create dr
df = pd.DataFrame(jokes)

# print top 5 rows
print(df.head(5))

# Notes:
# This dataset contains 10 jokes retrieved from the JokeAPI.
# The data includes the joke category, type, setup, and delivery.
# This dataset could be used to analyze the different types of jokes available.
# It could also be used to build a simple joke-generating application.
