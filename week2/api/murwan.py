import requests
import json
import pandas as pd

# API URL that returns 10 jokes
url = "https://v2.jokeapi.dev/joke/Any?amount=10"

# Get data from the API
response = requests.get(url)

# Convert the API response from JSON
data = response.json()

# Get the list of jokes
jokes = data["jokes"]

# Convert the jokes into a DataFrame
df = pd.DataFrame(jokes)

# Replace missing values with empty text
df = df.fillna("")

# Display the first 5 rows
print(df.head())

# This dataset contains jokes collected from JokeAPI.
# It includes information such as the joke category, type, and content.
# This data could be used to analyze different categories of jokes.
# It could also be used to build a simple joke application.