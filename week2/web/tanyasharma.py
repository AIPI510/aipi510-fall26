import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Download the webpage and identify its HTML table.
headers = {"User-Agent": "Mozilla/5.0 (compatible; TanyaGDP scraper)"}
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="wikitable")
if table is None:
	raise ValueError("Could not find the GDP table on the webpage")

# Convert the selected table into a pandas DataFrame.
data = pd.read_html(StringIO(str(table)))[0]
data.columns = ["Country/Territory", "IMF", "World Bank", "United Nations"]

# Remove footnotes, missing rows, repeated headers, and the World total.
data = data.replace(r"\[[^\]]*\]", "", regex=True).dropna()
data = data[data["Country/Territory"] != "Country/Territory"]
data = data[data["Country/Territory"] != "World"].reset_index(drop=True)

# Display the first five rows of the cleaned DataFrame.
print(data.head(5))

# This dataset lists nominal GDP estimates for countries and territories.
# It compares estimates from the IMF, World Bank, and United Nations.
# The data can be used to rank economies, compare sources, and create charts.
# The figures can help identify the world's largest economies.
# Insights can be drawn about economic trends, growth, and disparities between nations.