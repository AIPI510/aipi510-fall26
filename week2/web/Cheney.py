import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Download HTML from selected page
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# 2. Use BeautifulSoup to find the desired <table> and parse it into a DataFrame
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"class": "wikitable"})

# Parse the found table element into a Pandas DataFrame
df = pd.read_html(str(table))[0]

# 3. Clean the data (drop empty rows, clean repeated headers or unnamed columns)
if isinstance(df.columns, pd.MultiIndex):
  df.columns = df.columns.droplevel(0)

df = df.dropna(how="all")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# 4. Print the first 5 rows
print("--- First 5 rows of the scraped data ---")
print(df.head())

# 5. Add 3–5 lines of notes at the bottom of the script describing your data and how you might use it
# --- Data Notes ---
# This dataset contains global nominal Gross Domestic Product (GDP) statistics compiled directly from public tables.
# It can be utilized for macro-level economic analysis, evaluating national wealth, and comparing international market sizes.
# Potential use cases include building predictive economic models or visualizing regional income disparities in dashboard apps.
# Note that reporting timelines and currency conversion methods may vary slightly across international financial institutions.