import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist"
response = requests.get(url)

data = response.json()

extracted_data = {
    "category": data.get("category"),
    "type": data.get("type"),
    "joke": data.get("joke") if data.get("type") == "single" else f"{data.get('setup')} ... {data.get('delivery')}",
    "id": data.get("id"),
}

df = pd.DataFrame([extracted_data])

print(df.head())

#   This file retrives a joke from the JokeAPI and stores the joke along with its metadata in a pandas DataFrame.
#   The category, type, joke, and id. 
#   This data can be used to provide a joke for the user to brighten their day, but also analyze the metadata to ensure that the joke is appropriate for the user.