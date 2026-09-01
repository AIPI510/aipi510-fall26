import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://quotes.toscrape.com"
response = requests.get(url)
print(response.status_code)  # should be 200

soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("span", class_="text")
authors = soup.find_all("small", class_="author")

data = []
for quote, author in zip(quotes, authors):
    data.append({"quote": quote.text, "author": author.text})

df = pd.DataFrame(data)
df.to_csv("sabrina_quotes_data.csv", index=False)

print(df.head())

# Notes:
# - Scraped quotes and their authors from quotes.toscrape.com, a site built for
#   practicing web scraping.
# - Each row represents one quote-author pair pulled from the homepage's HTML.
# - This data could be used to build something like a random "quote of the day"
#   generator, or to analyze which authors are quoted most often across a larger
#   crawl of the site's multiple pages.
# - Limitation: this only grabs quotes from the first page — the site has multiple
#   pages of quotes that would need pagination to collect fully.