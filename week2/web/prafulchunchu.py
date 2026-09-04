# Web Scraping

import requests

from bs4 import BeautifulSoup

import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0"

})

# Force UTF-8 so accented player names (e.g. Dončić) ouput correctly
response.encoding="utf-8"

html = response.text

soup = BeautifulSoup(html, "html.parser")

# The page has multiple <table> tags — list them with their ids to find the right one
tables = soup.find_all("table")

for i, t in enumerate(tables):
    print(i, t.get("id")) # totals_stats is the table I'd like to select


# Grab the specific table by its id, rather than by position in the list
totals_stats_table = soup.find("table", id="totals_stats")
# The first <tr> in the table holds the column headers (<th> tags)
header_row = totals_stats_table.find("tr")
column_names = header_row.find_all("th")

# Pull clean text out of each header tag to build our column name list
features = []
for i, t in enumerate(column_names):
    features.append(t.get_text())
#     print(i, t.get_text())

# print(features)
# Every other <tr> after the header holds one player's stats
table_rows = totals_stats_table.find_all("tr")[1:]


all_rows = []

for rows in table_rows:
    cells = rows.find_all(["th","td"])
    row_data = []
    for cell in cells:
        row_data.append(cell.get_text())
    all_rows.append(row_data)


df = pd.DataFrame(all_rows, columns=features)



# Did not find any null values or repeated header rows in the table
print(df.isna().sum())
print(df[df["Player"] == "Player"])

# Convert object type data that are numeric and setting them to numeric dtype
numeric_cols = ["Age", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%",
                "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB",
                "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "Trp-Dbl"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df.head())


# Notes----------------------
# This table contains 2023-24 NBA season totals for every player who saw
# action that year (32 columns: box score stats, shooting percentages, awards).
# Each row is one player's full-season stat line; players traded mid-season
# may appear more than once (once per team).
# Checked for missing values and duplicate header rows — found none, so no
# rows needed to be dropped.
# Could be used to compare player performance, build stat-based rankings,
# or as a feature set for models predicting awards or team success.


