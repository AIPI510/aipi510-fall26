import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

response = requests.get(url, headers={"User-Agent": "aipi510-week2-student-script"})
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="wikitable")

df = pd.read_html(str(table))[0]

# Remove rows that contain no useful data.
df = df.dropna(how="all")

print(df.head())

# This dataset lists countries and their nominal gross domestic product.
# The data can be used to compare the sizes of national economies.
# I could create visualizations of the countries with the largest GDP values.
# It could also be combined with population data to analyze GDP per person.