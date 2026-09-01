import requests
from bs4 import BeautifulSoup
import pandas as pd


# Wikipedia blocks requests that don't send a real-looking User-Agent
# (the default one requests sends gets a 403 Forbidden) - so we spoof one here.
request_headers = {'User-Agent': 'Mozilla/5.0 (educational scraping exercise)'}
response = requests.get(
    "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)",
    headers=request_headers,
)
print('status:', response.status_code)  # should be 200 - if not, the page below will be empty

soup = BeautifulSoup(response.text, 'html.parser')

# Wikipedia tables usually carry class "wikitable" - find all of them
tables = soup.find_all('table', {'class': 'wikitable'})
print(len(tables))  # see how many there are, then pick the right index below

table = tables[0]  # index 0 = per-country GDP table; index 1 is regional groupings, not individual countries

# header row -> column names
headers = [th.text.strip() for th in table.find_all('tr')[0].find_all('th')]

# remaining rows -> data
rows = []
for tr in table.find_all('tr')[1:]:
    cells = [td.text.strip() for td in tr.find_all('td')]
    if cells:  # skip rows with no <td> (e.g. repeated header rows)
        rows.append(cells)

df = pd.DataFrame(rows, columns=headers)
print(df.head())

# Notes:
# - Data source: Wikipedia's "List of countries by GDP (nominal)" page, the per-country
#   table (not the regional-groupings table further down the page).
# - Each row is one country/territory, with nominal GDP estimates from three sources
#   side by side: IMF, World Bank, and the United Nations, each for a different year.
# - Values are scraped as raw strings (with footnote markers like "[1]" still attached
#   in some cells) - they'd need cleaning (strip footnotes, remove commas, cast to
#   numeric) before doing any real analysis or plotting.
# - Possible uses: rank countries by GDP, compare how the three sources' estimates
#   diverge for the same country, or join this against other per-country datasets
#   (population, GDP per capita) using "Country/Territory" as the join key.