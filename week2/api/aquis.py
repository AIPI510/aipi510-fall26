import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?amount=10&type=twopart"
response = requests.get(url)
response.raise_for_status()
data = response.json()

jokes = data["jokes"]
df = pd.DataFrame(jokes)
df = df[["category", "type", "setup", "delivery", "safe", "id"]]

print(df.head())

# This data contains jokes from several categories with a setuo and delivery.
# This could be used for some of the following purposes:
    # 1. Making a daily joke app. 
    # 2. analyzing number of jokes in each category.
    # 3. analyzing jokes by type. 
    # 4. analyzing jokes by safe or not safe.
