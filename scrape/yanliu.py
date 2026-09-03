import requests
from bs4 import BeautifulSoup
import pandas as pd

#1. HTTP request 
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)" 
response = requests.get(url, headers = {"User-Agent" :"Mozilla/5.0" })
html = response.text

#2. HTML Parsing by BeautifulSoup 
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")

# finding the right table 
# print(len(tables))
# for i, table in enumerate(tables):
#     print(f"Table {i}: {table.get_text()[:100]}")
# Table structure: 
# <table> <tr> <th> <td>  
table = tables[2]

#3. Data Extraction 
rows = table.find_all("tr")
header_cells = rows[0].find_all("th")
columns = [cell.get_text(strip=True) for cell in header_cells]

data = []
for row in rows[1:]:
    cells = row.find_all(["th", "td"])
    values = [cell.get_text(strip=True) for cell in cells]

    if len(values) == len(columns):
        data.append(values)

#4. from list to DataFrame
df = pd.DataFrame(data, columns=columns)
df =df.dropna()
df = df.drop_duplicates()

print(df.head())


# This dataset contains nominal GDP estimates for countries, including GDP values reported by the IMF, World Bank, and United Nations.
# The data could be used to compare the economy among different countries
# and to examine differences between GDP estimates from different organizations.








