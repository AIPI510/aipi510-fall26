# AIPI 510 - Week 2, Station 1: Web Scraping
# Ben Dushnitzky
# Scrapes the GDP (nominal) by country table from Wikipedia.
#
# AI use disclosure: I used Claude (Anthropic) to help write and debug this script,
# including adapting the table parsing after the live Wikipedia layout changed.

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Wikipedia blocks requests that don't look like a real browser, so set a User-Agent.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="wikitable")

# The header row is all <th> and the data rows are all <td>, but that has flipped
# around before on this page, so grab both kinds of cell and skip any row that has
# no <td> in it at all. That drops header rows without hardcoding how many there are.
rows = []
for tr in table.find_all("tr"):
    cells = tr.find_all(["th", "td"])
    if len(cells) >= 4 and tr.find("td"):
        rows.append([c.get_text(strip=True) for c in cells[:4]])

print("Rows scraped:", len(rows))

df = pd.DataFrame(rows, columns=["Country", "IMF", "WorldBank", "UN"])

# Each source's default year lives in its header cell, e.g. "IMF(2026)[1]".
# Pull those out instead of hardcoding them, since they change every year.
header_cells = [c.get_text(strip=True) for c in table.find_all("tr")[0].find_all(["th", "td"])]
default_years = [re.search(r"(\d{4})", h) for h in header_cells[1:4]]
default_years = [m.group(1) if m else None for m in default_years]
print("Default years from header:", default_years)

# A GDP cell is usually just "32,383,920", but when a source's figure is older than
# the column default it looks like "552,325 (2024)". Missing figures show up as "-N/a"
# with an em dash. So: split the year off, then clean the number.
for i, source in enumerate(["IMF", "WorldBank", "UN"]):
    raw = df[source]
    df[source + "_Year"] = raw.str.extract(r"\((\d{4})\)")[0].fillna(default_years[i])
    df[source + "_GDP"] = (raw.str.replace(r"\(\d{4}\)", "", regex=True)
                              .str.replace(",", "", regex=False)
                              .str.strip())

# Em dash means no data reported.
df = df.replace(r".*—.*", None, regex=True)

# Strip footnote markers like "[n 1]" off the country names.
df["Country"] = df["Country"].str.replace(r"\[.*?\]", "", regex=True).str.strip()

# Drop the "World" row, it's a total and not a country.
df = df[df["Country"] != "World"]

number_cols = ["IMF_GDP", "IMF_Year", "WorldBank_GDP", "WorldBank_Year", "UN_GDP", "UN_Year"]
for col in number_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df[["Country"] + number_cols]
df = df.dropna(subset=["IMF_GDP"]).reset_index(drop=True)

print("Rows after cleaning:", len(df))
print()
print(df.head())

# Notes on the data:
# Each row is one country/territory with its nominal GDP in millions of USD as estimated
# by three different sources (the IMF, the World Bank, and the UN), plus the year each
# of those estimates is actually for. The three sources disagree and are not all from the
# same year, which is the interesting part -- I could compare them to see how much
# "the" GDP of a country depends on who you ask. It would also work as a country-level
# feature to join onto other datasets, or as a denominator for per-capita normalization.
