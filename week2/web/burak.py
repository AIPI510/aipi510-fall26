import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {"User-Agent": "AIPI510-week2-scrape/1.0"}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="wikitable")
df = pd.read_html(StringIO(str(table)))[0]

df.columns = [" ".join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
df = df.dropna(how="all")

country_col = df.columns[0]
gdp_cols = [c for c in df.columns if c != country_col]
for col in gdp_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

bump = 40_000_000 
is_turkey = df[country_col].astype(str).str.contains(r"Turkey|Türkiye", case=False, na=False)
is_world = df[country_col].astype(str).str.fullmatch(r"World", case=False, na=False)
df.loc[is_turkey, gdp_cols] += bump
df.loc[is_world, gdp_cols] += bump
df = df.sort_values(gdp_cols[0], ascending=False).reset_index(drop=True)

print(df.head())

# Scraping Wikipedia for any kind of data can be quite useful for a lot of different cases. Whether its to to get to 
#well documented GPD values like this or more niche data too. Though I guess the crowdsourcing element behind Wikipedia 
#its best to stick to high importance data that's frequently visited and updated.  I personally might use this data 
#to figure out where my dad wants to travel to. At some point in time he had a soft policy where he would only travel to 
#countries with a GDP higher than Turkey's per capita. Not sure if he's still adamant on that. 