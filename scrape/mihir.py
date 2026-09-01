import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.scrapethissite.com/pages/forms/"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# The stats table on this site has this class
table = soup.find("table", {"class": "table"})

# Use pandas to parse the table HTML directly into a DataFrame
df = pd.read_html(str(table))[0]

# Clean up column names (strip whitespace/newlines from headers)
df.columns = [c.strip() for c in df.columns]

# Drop only rows missing essential fields (OT Losses is often blank
# for older seasons before the NHL tracked overtime losses)
df = df.dropna(subset=["Team Name", "Year", "Wins", "Losses"])

# Reset index after filtering
df = df.reset_index(drop=True)

print(df.head())

# --- Notes ---
# This dataset contains team-level NHL stats by season (wins, losses, goals
# for/against, etc.) scraped from a site built for scraping practice, so it
# only returns one page (25 rows) at a time without pagination handling.
# I could use this to compare team performance across seasons, calculate
# derived metrics like goal differential, or extend the script to loop
# through all pages for the full historical dataset.
# One limitation: this is practice/sample data, not live current-season
# stats, so it's useful for learning the scraping workflow but not for
# up-to-date analysis.