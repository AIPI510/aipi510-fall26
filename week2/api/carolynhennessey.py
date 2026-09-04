import requests
import json
import pandas as pd

def fetch_data():
    """
    Calls open weather api and returns JSON response
    """
    url = "https://openlibrary.org/search.json?q=test"
    response = requests.get(url)

    return response.json()

def create_df(json_data):
    """
    Receives json input and returns a pandas dataframe
    """

    df = pd.DataFrame(json_data.get("docs"))

    return df

if __name__ == "__main__":
    data = fetch_data()

    df = create_df(data)


    print(df.head())

# This script, similarly to the the scraping script, would be useful when I needed access to live data that I expected to be updated often.
# I would typically prefer to use an API call since the format of the data returned is ensured by the API contract and would likely fail loudly if changed.
# As a software developer, looking for an API before scraping would be my first choice.


