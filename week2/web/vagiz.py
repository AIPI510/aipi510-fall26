"""Script for taking GPD data from wiki. Specify headers as required by wiki policy."""

import requests

from bs4 import BeautifulSoup as bs

import pandas as pd


def get_url_content(url: str):
    headers = {
        "User-Agent": "MyDataScraperBot/1.0 (contact: vagiz.daudov@duke.edu) Python-requests"
    }
    response = requests.get(URL, headers=headers)
    soup = bs(response.text, "html.parser")

    table = soup.find("table")
    
    df = pd.read_html(str(table))[0]

    df.dropna(inplace=True)
    return df


if __name__ == "__main__":
   URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
   df = get_url_content(URL)
   print(df.head())


# Note
# Note
# Note

