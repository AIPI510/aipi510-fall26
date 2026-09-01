import sys

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Windows consoles default to cp1252 and cannot print accented player names.
sys.stdout.reconfigure(encoding="utf-8")

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response = requests.get(url)
response.raise_for_status()
# The server sends no charset, so requests falls back to ISO-8859-1 and mangles
# accented player names (Doncic becomes mojibake). The page is really UTF-8.
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "lxml")
# Two tables on the page: totals_stats (regular season) and totals_stats_post (playoffs).
table = soup.find("table", id="totals_stats")

header_row = table.find("thead").find("tr")
columns = [th.get_text() for th in header_row.find_all("th")][1:]  # Exclude the first column (rank)
data = []
for row in table.find("tbody").find_all("tr"):
    cells = row.find_all("td")
    row_data = [cell.get_text() for cell in cells]
    data.append(row_data)

df = pd.DataFrame(data, columns=columns)

# --- Cleaning ---

# 1. The last row is a "League Average" aggregate, not a player. Dropped it.
df = df[df["Player"] != "League Average"]

# 2. Players traded mid-season appear multiple times: one combined row with Team
#    "2TM"/"3TM" holding their full-season totals, plus one row per team they
#    played for. Keeping all of them would double-count those players. I kept
#    the combined row so each player appears exactly once with correct season
#    totals, at the cost of losing team attribution for traded players.
COMBINED = ("2TM", "3TM")
traded = set(df.loc[df["Team"].isin(COMBINED), "Player"])
df = df[~(df["Player"].isin(traded) & ~df["Team"].isin(COMBINED))]

# 3. Every column arrived as text. Convert the stat columns to numbers.
#    errors="coerce" turns blanks into NaN instead of raising.
text_cols = ["Player", "Team", "Pos", "Awards"]
numeric_cols = [c for c in df.columns if c not in text_cols]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

#    Note: I deliberately do NOT dropna(). Blank percentage columns mean the
#    player never attempted that shot (0/0 is undefined, not zero), and Awards
#    is blank for most players. Dropping those rows would discard ~100 valid
#    players and destroy the sample.

df = df.reset_index(drop=True)

print(df.shape)
print(df.head())

"""
This data is 2023-2024 NBA regular season totals scraped from basketball-reference.com. It includes all players who played in the 2023-2024 NBA season, with their total statistics for the season.

I kept the combined 2TM/3TM rows for players who were traded mid-season, and dropped the individual team rows for those players to avoid double-counting. The last row, which is a "League Average" aggregate, has also been dropped.

I did not drop rows with NaN values in percentage columns or the Awards column, as those represent valid cases (e.g., a player who never attempted a certain type of shot).

This data could be used downstream for analysis, such as calculating averages, comparing player performance, or building predictive models.

"""
