import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"
response =requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
tables = soup.find_all("table")

df = pd.read_html(StringIO(str(tables[0])))[0]

print("First 5 rows:")
print(df.head())