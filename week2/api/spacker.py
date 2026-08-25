import requests
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any?type=single&amount=5"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers).json()

df = pd.DataFrame.from_dict(response['jokes'])

print("Here are 5 random jokes:")
print(df['joke'])

# This just prints out 5 random jokes from the JokeAPI
# Possible use cases are to use this to add an Easter egg to an application with your joke
# It could potentially be expanded to include single and two part jokes