"""
AIPI 510 - Week 2 Sync Activity
file: caleb.py

This python file web scrapes data from Quotes.toScrape.com and parses the data into a pandas DataFrame.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get("https://quotes.toscrape.com/")

quote_scrape = response.text
quote_soup = BeautifulSoup(quote_scrape, 'html.parser')

title = quote_soup.find('title').text
print(title)

quote_rows = []

for item in quote_soup.find_all("div", class_='quote'):
    quote = item.find("span", itemprop='text')
    author = item.find("small", class_='author')

    quote_rows.append({
        "quote": quote.get_text(" ", strip=True),
        "author": author.get_text(" ", strip=True)
    })

df = pd.DataFrame(quote_rows)

print(df.head())

"""
I would use the quotes in this DataFrame as a daily inspirational topic or conversation
starter for group projects or classes. I would also use the quotes for daily updates to a 
website that highlighted the creativity and originality of humanity.
"""

