import requests
import json
import pandas as pd
url = "https://official-joke-api.appspot.com/jokes/ten"

response = requests.get(url)

print(response.status_code)

data = response.json()
print(data) #just to see the data for yourself in json format 

df = pd.DataFrame(data)
print(df.head())

# This dataset contains jokes from the Official Joke API.
# Each joke includes a type, setup, punchline, and ID.
# The data could be used to analyze different types of jokes
# or build a simple joke recommendation application.