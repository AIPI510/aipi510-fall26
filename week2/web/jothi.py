import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))

table = soup.find('table', class_='stats_table')

# Getting the df headers
headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())
    if th.text.strip() == 'Awards':
        break
headers = headers[1:]

#print("Columns:", headers)

# Getting the df content 
all_rows = table.find_all("tr")[1:]
rows_data = []

for tr in all_rows:
    cells = tr.find_all("td")
    if cells:
        row_text = [cell.text.strip() for cell in cells]
        rows_data.append(row_text)

df = pd.DataFrame(rows_data, columns=headers)

print(df)
df.head(10)


"""
This script can be used to scrape the scores and ranking of various players in the NBA.
It will source data from the NBA website on statistics of each player.
It will be documented here.
"""
