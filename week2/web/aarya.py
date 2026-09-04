"""Scrape a public country GDP table from Wikipedia."""

# %%
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
HEADERS = {"User-Agent": "AIPI510-data-sourcing-assignment"}

# Download the webpage using PAGE_URL, HEADERS, and a 30-second timeout.
response = requests.get(url=PAGE_URL, headers=HEADERS, timeout=30)
response.raise_for_status()

# Parse response.text with BeautifulSoup and the html.parser parser.
soup = BeautifulSoup(response.text, "html.parser")

# Find all tables whose class is "wikitable".
wiki_tables = soup.find_all("table", class_="wikitable")

# Select the country table rather than the separate regional table.
country_table = next(
    table for table in wiki_tables if "Country/Territory" in table.get_text()
)

# Use pd.read_html() to turn country_table into a DataFrame.
# StringIO lets pandas read the selected table's HTML as text.
gdp_df = pd.read_html(StringIO(str(country_table)))[0]
gdp_df
# %%
# Remove citation markers such as [1] and [n 1] from column/country names.
gdp_df.columns = gdp_df.columns.str.replace(r"\[.*?\]", "", regex=True)
gdp_df["Country/Territory"] = (
    gdp_df["Country/Territory"].str.replace(r"\[.*?\]", "", regex=True).str.strip()
)

# Remove the aggregate "World" row and duplicate country rows.
gdp_df = gdp_df[gdp_df["Country/Territory"] != "World"]
gdp_df = gdp_df.drop_duplicates(subset="Country/Territory")

print(gdp_df.head(5).to_string(index=False))

# One row represents a country's estimated gross domestic product.
# The table makes it possible to compare the economic output of different countries.
# One limitation is that GDP estimates may use different methods, years, or exchange
# rates, so comparisons do not capture every difference in living standards.
