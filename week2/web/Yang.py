import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")

gdp_table = None

for table in tables:
    table_text = table.get_text()

    if "Country/Territory" in table_text and "IMF" in table_text:
        gdp_table = table
        break

if gdp_table is None:
    raise Exception("Could not find the GDP table.")

df = pd.read_html(str(gdp_table))[0]

# Clean the data
df = df.dropna(how="all")
df = df.drop_duplicates()

# Flatten column names if pandas creates multi-level columns
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [
        "_".join([str(part) for part in col if str(part) != "nan"]).strip()
        for col in df.columns
    ]

# Remove repeated header rows if they appear inside the table
first_col = df.columns[0]
df = df[df[first_col].astype(str) != str(first_col)]

csv_file = "Yang_gdp_data.csv"
df.to_csv(csv_file, index=False)

print("First 5 rows:")
print(df.head())

print("\nData saved to", csv_file)


# Notes:
# I scraped nominal GDP data from a Wikipedia table using requests and BeautifulSoup.
# I converted the HTML table into a pandas DataFrame.
# I cleaned the data by dropping empty rows, duplicates, and repeated header rows.
# This dataset could be used to compare countries by economic size.
# In a larger project, I could combine GDP data with population data to analyze GDP per capita.
