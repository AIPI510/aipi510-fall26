import requests
import json
import pandas as pd

# JokeAPI: fetch 10 safe programming jokes (docs: https://jokeapi.dev)
url = "https://v2.jokeapi.dev/joke/Programming?safe-mode&amount=10"

response = requests.get(url)
response.raise_for_status()
data = response.json()

# Each joke is either one-liner ("single") or setup/delivery ("twopart")
rows = []
for joke in data["jokes"]:
    if joke["type"] == "single":
        text = joke["joke"]
    else:
        text = joke["setup"] + " ... " + joke["delivery"]
    rows.append({"id": joke["id"], "category": joke["category"], "type": joke["type"], "joke": text})

df = pd.DataFrame(rows)
print(df.head())

# Notes:
# Data pulled from JokeAPI (v2.jokeapi.dev): 10 programming jokes per run, with id,
# category, type (single vs twopart), and the joke text. Results change on every
# request since the API serves random jokes. Could be used to build a joke dataset over repeated calls, or to compare joke types/categories for a text analysis demo.