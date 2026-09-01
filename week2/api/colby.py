import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist"
response = requests.get(url)

data = response.json()

df = pd.DataFrame([data])
print(df.head())

'''
    This file retrives a joke from the JokeAPI and stores the joke along with its metadata in a pandas DataFrame.
    The error tag, category, type, joke, flags, saftey tag, id, and language are retrieved. 
    This data can be used to provide a joke for the user to brighten their day, but also analyze the metadata to ensure that the joke is appropriate for the user.
'''