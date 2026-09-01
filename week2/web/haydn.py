import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Premier_League"

# Wikipedia blocks the default python-requests User-Agent (403), so a
# browser-like one is required.
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # The page has several tables with class "wikitable" (stadiums, kits,
    # managers, ...); the league standings table is the one whose header row
    # starts with "Pos".
    table = None
    for candidate in soup.find_all("table", {"class": "wikitable"}):
        first_header = candidate.find("th")
        if first_header and first_header.text.strip() == "Pos":
            table = candidate
            break

    # Only keep the core standings columns. The table also has a merged
    # "Qualification or relegation" column (rowspan cells) and per-opponent
    # result columns that don't line up one-to-one with the header row, so
    # they're dropped rather than misaligned.
    headers_row = table.find("tr")
    column_names = [th.text.strip() for th in headers_row.find_all("th")][:10]

    rows = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all(["th", "td"])[:10]
        if len(cells) == len(column_names):
            rows.append([cell.text.strip() for cell in cells])

    df = pd.DataFrame(rows, columns=column_names)

for i in range(5):
    print(df.iloc[i])  # print the first 5 lines (Step 7)

'''
This is the 2025-26 Premier League standings table, scraped from Wikipedia. 
Since it's mid-season, standings reflect games played so far rather than a final table.
One use case is to track a team's form over the season by re-scraping periodically,
compare goal difference/points to build a simple league predictor, or join
this with match-level data to analyze how individual results shift table
position.
'''
