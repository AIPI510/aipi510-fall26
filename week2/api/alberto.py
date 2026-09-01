import requests
import json
import pandas as pd

# First we define the API URL
apiUrl = "https://v2.jokeapi.dev/joke/Any?type=single&amount=10&safe-mode"

# Now we make a GET request to the API
response = requests.get(apiUrl)

# We convert the JSON response into Python data
data = response.json()

# Now we store the jokes in a DataFrame
jokesData = pd.DataFrame(data["jokes"])

# We keep the fields that are useful for our dataset
jokesData = jokesData[["category", "type", "joke", "id", "safe", "lang"]]

# Finally, we print the first 5 rows
print(jokesData.head())

# This dataset contains jokes collected from JokeAPI.
# Each row represents one joke with information about its category and language.
# The data could be used to analyze which joke categories are more common.
# It could also be used to build a simple joke recommendation application.