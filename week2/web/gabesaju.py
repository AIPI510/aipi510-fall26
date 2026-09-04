import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {"User-Agent": "Mozilla/5.0 (Duke AIPI510 coursework)"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"class": "wikitable"})

rows = []
for tr in table.find_all("tr"):
    cells = [c.get_text(strip=True) for c in tr.find_all(["th", "td"])]
    if cells:
        rows.append(cells)

# Row 0 is the header
columns = ["country", "imf_estimate", "world_bank_estimate", "un_estimate"]
df = pd.DataFrame(rows[1:], columns=columns)

#strip wiki footnote markers
df["country"] = df["country"].str.split("[").str[0].str.strip()

#wiki uses em dashes for missing values
df = df.replace(["—", "-", ""], pd.NA)

#drop the agregate world row since its not a country
df = df[df["country"] != "World"]

#gdp values arrive as comma separated strings so we need to strip the seperators
money_cols = ["imf_estimate", "world_bank_estimate", "un_estimate"]
for col in money_cols:
    df[col] = df[col].str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")

#drop rows with no IMF figure, then convert that column to numbers
df = df.dropna(subset=["imf_estimate"])
df["imf_estimate"] = df["imf_estimate"].astype(int)

df = df.reset_index(drop=True)

print(df.head())

# Notes
# source: Wikipedia "List of countries by GDP (nominal)"
# each row is one country with three nominal GDP estimates in millions of USD from the IMF, World Bank and UN.
# The three sources report different reference years (2024-26) so the columns are not directly comparable without accounting for that gap. 
# A few countries do not have IMF figures and are getting dropped during cleaning
# This could be used to join to population data for GDP per capita or compare the three sources against each other to quantify disagreement between bodies.