import requests
import json
import pandas as pd


url = "https://v2.jokeapi.dev/joke/Any"

jokes = []

for i in range(5):
    params = {
        "type": "single"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    row = {
        "category": data["category"],
        "joke": data["joke"],
        "safe": data["safe"],
        "language": data["lang"]
    }

    jokes.append(row)


df = pd.DataFrame(jokes)

print("First 5 rows:")
print(df.head())

csv_file = "Yang_joke_data.csv"
df.to_csv(csv_file, index=False)

print("\nData saved to", csv_file)


# Notes:
# I collected joke data from the public JokeAPI using HTTP GET requests.
# The dataset contains joke category, joke text, safety status, and language.
# I stored five API responses in a pandas DataFrame and saved them as a CSV file.
# This data could be used to analyze joke categories or build a simple entertainment application.
# The API does not require an API key, making it easy to access for this exercise.
