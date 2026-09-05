import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "AIPI510-Student-Scraper/1.0 (raul.cepin@duke.edu)"
}

response = requests.get(
    "https://en.wikipedia.org/wiki/List_of_killings_by_law_enforcement_officers_in_the_United_States_in_the_1990s",
    headers=headers
)
response.raise_for_status()  # stop with a clear error if the request failed

soup = BeautifulSoup(response.text, "html.parser")

# Step 6: find the data table (one wikitable covers the whole decade on this page)
tables = soup.find_all("table", class_="wikitable")
print(f"Found {len(tables)} tables")

# Loop over the table rows, collecting cleaned cell text.
# Rows without exactly 4 td cells (headers, malformed rows) are skipped.
all_rows = []
for table in tables:
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 4:
            all_rows.append([cell.get_text(strip=True) for cell in cells])

# Build the DataFrame
df = pd.DataFrame(all_rows, columns=["Date", "Name", "State", "Description"])

# Step 7: clean the data
df["Description"] = df["Description"].str.replace(r"\[\d+\]", "", regex=True).str.strip()  # remove citation markers like [1]
df = df.replace("", pd.NA)                 # turn empty strings into real missing values
df = df.dropna(subset=["Date", "Name"])    # drop rows missing the essentials
df = df[df["Date"] != "Date"]              # remove any repeated header rows

# Step 8: print the first 5 rows
print(df.head())
print(f"\nTotal rows after cleaning: {len(df)}")

# Step 9: Notes
# This dataset contains killings by law enforcement officers in the US during the 1990s, scraped from Wikipedia's decade list page (582 rows spanning 1990-01 to 1999-12-31).
# Columns: Date, Name (and age), State (with city), and Description where available.
# Cleaning: citation markers like [1] were stripped; rows without exactly 4 cells were skipped.
# Limitations: Wikipedia notes the list is incomplete, coverage is skewed toward later years and dates have mixed precision (some entries are year-month only).
# Possible uses: analyzing trends by year or state, or joining with population data to compare rates across states.