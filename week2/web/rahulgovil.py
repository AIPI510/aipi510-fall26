import io
import pandas as pd
import requests
from bs4 import BeautifulSoup

# scrape data from basketball reference
url = "https://www.basketball-reference.com/teams/DET/2026.html"

response = requests.get(url, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

table = soup.select_one("table#per_game_stats")
if table is None:
    raise ValueError("Stats table not found on the page.")

# convert to data frame and drop unnecessary columns
df_list = pd.read_html(io.StringIO(str(table)))
df = df_list[0]
df.drop(columns=["Rk", "Awards"], inplace=True)

print(df.head())

'''
This script pulls the per-game averages of the Detroit Pistons players for the 2026 season from Basketball Reference.
The data contains their name, shooting percentages, assists and rebounds, and other relevant information. This information,
alongside other information from the same link, can be used to analyze the team and its players, for analytics such as player
impact and performance. Modeling can also be done by mapping the height and weight information to production based on the position
that the player plays. This can help optimize the roster for best performance.
'''