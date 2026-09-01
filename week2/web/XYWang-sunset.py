import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

response =requests.get(url)

soup = BeautifulSoup(response.text,"html.parser")
tables = soup.find_all("table")

df = pd.read_html(str(tables[0]))[0]
df = df.dropna(how="all")
df = df.reset_index(drop=True)

print("First 5 rows:")
print(df.head())