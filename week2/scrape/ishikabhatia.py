import requests
from bs4 import BeautifulSoup
import pandas as pd

#download the webpage and raw HTML data
url = "https://www.basketball-reference.com/teams/NYK/2024.html#all_per_game_stats_post"
response = requests.get(url)

#use beautifulsoup to parse the HTML data
soup = BeautifulSoup(response.content, 'html.parser')
#print(response.status_code)

#find the table containing the GDP data
table = soup.find('table', id = "per_game_stats_post")

#convert the table to a pandas dataframe
df = pd.read_html(table.prettify())[0]
df_drop_any = df.dropna(axis=1, how="any")
print(df_drop_any.head())


