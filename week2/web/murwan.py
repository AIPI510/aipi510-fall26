import requests
from bs4 import BeautifulSoup
import pandas as pd

# Webpage that contains the NBA player statistics
url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

# Download the webpage
response = requests.get(url)

# Read and parse the webpage HTML
soup = BeautifulSoup(response.content, "html.parser")

# Find the table on the webpage
table = soup.find("table")

# Convert the HTML table into a pandas DataFrame
df = pd.read_html(str(table))[0]

# Remove any repeated header rows
df = df[df["Rk"] != "Rk"]

# Replace missing awards with "None"
df["Awards"] = df["Awards"].fillna("None")

# Display the first 5 rows
print(df.head())

# This dataset shows NBA player statistics for the 2023 to 2024 season.
# It includes information such as each player's team, position, games played, and total points.
# I could use this data to compare the performance of different players.
# It could also help analyze which players performed best in different statistical categories.