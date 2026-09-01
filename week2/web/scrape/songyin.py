import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# URL of the webpage containing the GDP table
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Add a User-Agent so Wikipedia accepts the request
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download the webpage
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all Wikipedia tables
tables = soup.find_all("table", class_="wikitable")

# Select the first GDP table
table = tables[0]

# Convert the HTML table into a pandas DataFrame
df = pd.read_html(StringIO(str(table)))[0]

# Clean the data
df = df.dropna(subset=[df.columns[0]])

# Print the first 5 rows
print(df.head())

# Notes:
# This dataset contains nominal GDP information for countries around the world.
# It can be used to compare the economic size of different countries.
# The data could be used for economic analysis and visualization.
# For example, I could create charts comparing GDP across countries or regions.
# For example, I could create charts comparing GDP across countries or regions.