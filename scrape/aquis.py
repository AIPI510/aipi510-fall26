import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", id="totals_stats")
df = pd.read_html(str(table), flavor="lxml")[0]

df = df.dropna()
df = df[df.iloc[:, 0] != df.columns[0]]

print(df.head(5))

# The dataframe This data conatains NBA player stats for the 2023–2024 season
# Possible uses for this data include:
    # 1. Calculating per game averages for players
    # 2. Per-minute statistics for players
    # 3. Usage stats for players 
    # 4. Team aggregate stats based on individual player stats
