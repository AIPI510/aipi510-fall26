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
# This is NHL team stats by season (wins, losses, goals for/against) from
# a practice scraping site. It only grabs one page of 25 rows at a time.
#
# I could use this to compare teams across seasons or calculate stats like
# goal differential. To get more data, I'd need to loop through the site's
# other pages.
#
# Limitation: this is sample/practice data, not real current NBA/NHL stats,
# so it's good for learning scraping but not for real analysis.