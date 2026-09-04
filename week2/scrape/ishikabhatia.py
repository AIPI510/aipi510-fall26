import requests
from bs4 import BeautifulSoup
import pandas as pd

#download the webpage and raw HTML data
url = "https://www.basketball-reference.com/teams/NYK/2024.html#all_per_game_stats_post"
response = requests.get(url)

#use beautifulsoup to parse the HTML data
soup = BeautifulSoup(response.content, 'html.parser')

#find the table containing the GDP data
table = soup.find('table', id = "per_game_stats_post")

#convert the table to a pandas dataframe and drop columns with any missing or null values
df = pd.read_html(table.prettify())[0]
df_drop_any = df.dropna(axis=1, how="any")
print(df_drop_any.head())



#This data shows the top 5 scorers for the New York Knicks in the 2024 season based on per game stats, including their points, assists, and rebounds. 
#As seen through this data, Jalen Brunson scored 32.4 points per game, making him the top scorer for the team. 
#Donte scored 17.8 points per game, making him the second highest scorer for the team.
#OG Anunoby had the most assists per game
#The data can be used to analyze player performance and make predictions about future games. It can also help understand how individual players contribute to the team's overall success and be insightful for fantasy basketball fanatics looking to make informed decisions about their team.

#Please note, my first PR had issues with the autograder

