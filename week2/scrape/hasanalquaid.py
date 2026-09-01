import requests
from bs4 import BeautifulSoup
import pandas as pd

# Station 1
#Use requests.get(url) to download HTML from your selected page.
url = "https://www.basketball-reference.com/leagues/NBA_2026_totals.html"
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0"
})
html = response.text

# Use BeautifulSoup to find the desired <table> and parse it into a DataFrame.
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", {"id": "totals_stats"})
df = pd.read_html(str(table))[0]

# Clean the data (e.g., drop rows with missing values or headers repeated in the table).
df = df[df["Rk"] != "Rk"]        
df = df.dropna()  

# Print the first 5 rows.
print(df.head(5))

#Add 3–5 lines of notes at the bottom of the script describing your data and how you might use it.
# This dataset contains total season statistics for NBA players (2025-2026 season),
# including points, rebounds, assists, and other counting stats per player.
# Players who were traded mid-season may appear in multiple rows (once per team).
# Any player whose rows had a nan value were dropped.
# I could use this data to compare player performance across teams, identify
# statistical leaders in specific categories, or build a simple ranking/filtering tool.