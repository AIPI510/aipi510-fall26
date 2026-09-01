import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?amount=10"
response = requests.get(url)
response.raise_for_status()

data = response.json()
jokes = data["jokes"]

df = pd.DataFrame([
    {
        "id": joke.get("id"),
        "category": joke.get("category"),
        "type": joke.get("type"),
        "joke": joke.get("joke") if joke.get("type") == "single" else joke.get("setup"),
        "delivery": joke.get("delivery") if joke.get("type") == "twopart" else None,
        "safe": joke.get("safe"),
        "lang": joke.get("lang"),
    }
    for joke in jokes
])
pd.set_option("display.max_colwidth", None)
print(df[["joke", "delivery"]].head())
print(df.head())

#Possible uses: Creating joke generators. Censoring content that's is deemed offensive, unsafe or inappropriate. 
#