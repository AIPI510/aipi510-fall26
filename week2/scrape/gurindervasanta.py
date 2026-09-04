import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint

raw = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_totals.html').content
soup = BeautifulSoup(raw,'html.parser')
table = soup.find('table')
df = pd.read_html(str(table))[0]
df = df[~df['Team'].str.contains('TM$',na=False)]
df.to_csv('temp1.csv',encoding='utf-8')
print(df.head())

# NOTE: 
# This data provides several statistics regarding every NBA player's 2023-2024 season. 
# The statistics are totals across every important category in the game of basketball, as well as any awards they got. 
# It is important to note that if a player changes teams during the season, there will be 2 entries, 
# one entry for the totals on their first team and another entry for the totals on the second team. 
# This data could be useful for front offices who are trying to build out their bench depth since they can see how 
# the role players they are targetting are performing in their roles. 
