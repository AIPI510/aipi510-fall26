import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'id': 'totals_stats'})

df = pd.read_html(io.StringIO(str(table)))[0]

df["PTS"] = pd.to_numeric(df["PTS"])
top_5 = df.sort_values(by="PTS", ascending=False).head(5)

print(top_5[["Rk", "Player", "PTS"]])


# This script pull player stats from the 2023-2024 NBA season, specifically focusing on the top 5 players based on total points.
# The data is stored in a pandas DataFrame, with each row containing the player's rank, name, and total points scored.
# The data can be used to compare each top 5 player in a barchart to visualize the differences in points scored.