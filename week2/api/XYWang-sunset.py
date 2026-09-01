import requests
import json
import pandas as pd

# Step 5: Choose an API and read the documentation
# We use JokeAPI to retrieve jokes in JSON format.
url = "https://v2.jokeapi.dev/joke/Any?amount=10&safe-mode"

# Step 6: Make a GET request
response = requests.get(url)

# Check whether the request was successful
print("Status code:", response.status_code)

# Parse the JSON response
data = response.json()

# Store relevant fields into a DataFrame
jokes = []

for joke in data["jokes"]:
    if joke["type"] == "single":
        joke_text = joke["joke"]
    else:
        joke_text = joke["setup"] + " " + joke["delivery"]

    jokes.append({
        "id": joke["id"],
        "category": joke["category"],
        "type": joke["type"],
        "joke": joke_text,
        "language": joke["lang"]
    })

df = pd.DataFrame(jokes)

# Step 7: Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())
