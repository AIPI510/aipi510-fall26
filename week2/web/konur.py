import requests
from bs4 import BeautifulSoup
import pandas as pd

# Generated with the use of AI (ChatGPT)

url = "https://www.espn.com/nfl/team/depth/_/name/pit"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")

all_rows = []

for i, table in enumerate(tables):

    # Find tables containing the actual depth-chart players
    headers = [
        th.get_text(" ", strip=True)
        for th in table.find_all("th")
    ]

    if "Starter" not in headers:
        continue

    # ESPN puts the positions in the table immediately before this one
    position_table = tables[i - 1]

    positions = [
        row.get_text(" ", strip=True)
        for row in position_table.find_all("tr")
        if row.get_text(" ", strip=True)
    ]

    player_rows = [
    row for row in table.find_all("tr")
    if row.find_all("td")
    ]

    for position, row in zip(positions, player_rows):

        cells = row.find_all("td")

        if not cells:
            continue

        players = []

        for cell in cells[:3]:
            # Player names are links.
            # Using the <a> text avoids things like Q, IR, etc.
            player = cell.find("a")

            if player:
                players.append(player.get_text(strip=True))
            else:
                players.append("-")

        # Make sure there are always 3 depth-chart entries
        while len(players) < 3:
            players.append("-")

        all_rows.append({
            "Position": position,
            "Starter": players[0],
            "2nd": players[1],
            "3rd": players[2]
        })


df = pd.DataFrame(all_rows)

# Clean data
df = df.drop_duplicates()
df = df.reset_index(drop=True)

print(df.head())

# This web scraping script pulls the Steelers depth chart from ESPN.com. 
# It shows the order of depth at each position, beginning with the starting
# player, then their backup, and the backup's backup. If no name exists for 
# a particular depth level, use the "-" character. We might use this data 
# for sports analytics, or a machine learning model trained on the Steelers
# roster. 