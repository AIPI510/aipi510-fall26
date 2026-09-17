import requests
from bs4 import BeautifulSoup
import pandas as pd

# set page
url = 'https://www.basketball-reference.com/leagues/NBA_2024_totals.html'

# download html
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# find all tables
tables = soup.find_all("table")

# select table containig nba standings
table = None
for t in tables:
    if "Team" in t.get_text():
        table = t
        break

# extract rows from table
rows = table.find_all("tr")

# xtract headers
headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]

# extract data
data = []
for row in rows[1:]:
    cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
    if cells:
        data.append(cells)

# create df
df = pd.DataFrame(data)

# set column headers
if len(headers) == len(df.columns):
    df.columns = headers

# clean data
df = df.dropna(how="all")
df = df.drop_duplicates()

# print top 5 rows
print(df.head(5))


# Notes:
# This dataset contains NBA team standings from the 2023–24 season.
# The data includes information such as team names, wins, losses, and winning percentage.
# I could use this dataset to compare team performance during the season.
# It could also be used to create visualizations or analyze trends in team success.