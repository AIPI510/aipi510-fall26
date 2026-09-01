import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# First we define the webpage URL
url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

# Now we download the HTML from the webpage
response = requests.get(url)

# We parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# We find the table with player statistics
table = soup.find("table")

# We convert the table into a DataFrame
playersData = pd.read_html(StringIO(str(table)))[0]

# We remove repeated header rows from the table
playersData = playersData[playersData["Player"] != "Player"]

# We remove rows with missing player names
playersData = playersData.dropna(subset=["Player"])

# Finally, we print the first 5 rows
print(playersData.head())

# This dataset contains NBA player statistics from the 2023-24 season.
# Each row represents a player and includes different performance statistics.
# The data could be used to compare the performance of NBA players.
# It could also be used to analyze scoring and other player statistics.