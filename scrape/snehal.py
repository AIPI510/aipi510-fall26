#station 1 (pulling data from web)
import requests 
from bs4 import BeautifulSoup
import pandas as pd
url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")
df = pd.read_html(str(table))[0]
df = df.dropna()
print(df.head())

# This dataset contains NBA player statistics from the 2024 season.
# It includes information such as games played, points, and awards.
# The data could be used to analyze player performance and compare players.


