import requests 
from bs4 import BeautifulSoup
import pandas as pd 

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get("https://www.espn.com/nba/team/stats/_/name/phi/philadelphia-76ers", headers = headers)

html = response.content
soup = BeautifulSoup(html, "html.parser")


df = pd.read_html(str(soup))[0]
df.to_csv("philadelphia_76ers_stats.csv", index=False)
print(df)
#gives you a list of the names of players and then go through and number them based on time in the game