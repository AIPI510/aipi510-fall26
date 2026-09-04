import requests
from bs4 import BeautifulSoup
import pandas as pd

# web page for scraping 
url = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

# getting content from webpage - download HTML from page
response = requests.get(url)

# Use BeautifulSoap to find desired table and parse into DF
soup = BeautifulSoup(response.text, "html.parser")
# find table
table = soup.find("table")

# convert HTML table to DF
# installed lmxl to parse html into a table  
df = pd.read_html(str(table))[0]

# how many total rows and columns
print(df.shape)

# check for missing values
print(df.isnull().sum())

# clean/filter the data
df = df.dropna(subset=["Player"])
df = df[df["Player"] != "Player"]

# print the first 5 rows 
print(df.head())


# This dataset contains NBA player statistics from the 2023-2024 season.
# It includes statistics such as points, rebounds, assists, and shooting percentages.
# The data could be used to compare player performance across different statistical categories.
# It could also be used to identify the top-performing players from the season.