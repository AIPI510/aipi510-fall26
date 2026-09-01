import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?amount=10"


response = requests.get(url)

data = response.json()

jokes = data["jokes"]

df = pd.DataFrame(jokes)

print(df.head())

# This data contains jokes from JokeAPI.
# It includes the category, type, and content of each joke.
# This data could be used to compare different joke categories.