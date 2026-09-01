import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="wikitable")

df = pd.read_html(StringIO(str(table)))[0]

df = df.dropna(how="all")

print(df.head())

# This data contains nominal GPS information for countries around the world
# It includes GDP ranking in the table
# This data could be used to compare the economic size of different countries