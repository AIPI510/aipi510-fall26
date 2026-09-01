import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Download webpage
headers = {
    "User-Agent": "AIPI510-Class-Project/1.0"
}

response = requests.get(url, headers=headers)

# Check that request worked
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the first Wikipedia data table
table = soup.find("table", class_="wikitable")

# Convert the HTML table into a DataFrame
df = pd.read_html(str(table))[0]

# Clean rows with missing data
df = df.dropna(how="all")

# Print first 5 rows
print(df.head())

# This dataset contains countries and their nominal GDP values.
# It can be used to compare the size of different national economies.
# I could use this data to rank countries by GDP or analyze economic differences.
# It could also be combined with population data to compare GDP per person.