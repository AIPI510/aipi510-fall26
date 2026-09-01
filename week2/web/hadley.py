import requests 
from bs4 import BeautifulSoup
import pandas as pd 

# HTTP Request
url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0"
})
html = response.text

# Find the table
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", {"id": "totals_stats"})
df = pd.read_html(str(table))[0]

# Clean the data
df = df[df["Rk"] != "Rk"]
df = df.dropna(subset=["Player"])
df = df.reset_index(drop=True)

# Print first 5 rows 
print(df.head())

# Notes
# This dataset contains statistics about all the players in the NBA for the 2023-24 season. These 
# statistics include age and team and also totals like blocks and points. This was scraped from 
# basketball-reference.com. Some ways you might use this are analyzing the performance of different 
# players or different teams. This can be useful for either sports analytics or just general interest/curiosity.