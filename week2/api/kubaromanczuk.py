import requests
import pandas as pd

URL = 'https://v2.jokeapi.dev/joke/Any?amount=5'

def getJokes():
    response = requests.get(URL)
    response.raise_for_status()

    data = response.json()
    jokes = data['jokes']

    for joke in jokes:
        # Filter dictionary to keep only keys where value is True
        true_flags = [flag for flag, is_true in joke['flags'].items() if is_true]
        # Store as a comma-separated string (or empty string "" if none are True)
        joke['flags'] = ", ".join(true_flags)

    df = pd.DataFrame(jokes)

    print(df.head())

if __name__ == "__main__":
    getJokes()


# It's used to get jokes that can be later displayed on the page
# The data can be filtered out not safe / nsfw
# The script merges flags field as it broke the dataframe 
# It created a new entry for each flag type