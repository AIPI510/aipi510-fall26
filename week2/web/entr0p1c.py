import requests
from bs4 import BeautifulSoup
import pandas as pd

# Web page to scrape
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Add a browser-like User-Agent so Wikipedia accepts the request
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download the webpage
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all tables on the page
tables = soup.find_all("table")

print("Number of tables found:", len(tables))

# Find the GDP table
gdp_table = None

for table in tables:
    headers_text = table.get_text(" ", strip=True)
    if "Country/Territory" in headers_text and "GDP" in headers_text:
        gdp_table = table
        break

# Check that the table was found
if gdp_table is None:
    raise ValueError("GDP table was not found.")

# Convert the HTML table into a pandas DataFrame
df = pd.read_html(str(gdp_table), header=0)[0]

# Clean the data
df = df.dropna(how="all")
df = df.drop_duplicates()

# Print the first 5 rows
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Notes:
# This dataset contains countries and territories ranked by nominal GDP.
# The data can be used to compare the economic size of different countries.
# It could also be used to study global economic patterns and rankings.
# The GDP year and source should be checked before using the data for analysis.