import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://wdi.worldbank.org/table/1.2"
NULL_INDICATOR = ".."


# Use requests.get(url) to download HTML from your selected page
def fetch_data():
    """
    Returns html response served at URL
    """
    response = requests.get(URL)

    if response.status_code != 200:
        raise RuntimeError("Failed to fetch from ", URL)

    html = response.text
    print("Successfully fetched HTML for ", URL)

    return html

# Use BeautifulSoup to find the desired <table> and parse it into a DataFrame.
# Clean the data (e.g., drop rows with missing values or headers repeated in the table).
def find_table_parse_df(html):
    """
    Accepts an html string and returns a cleaned pandas DataFrame
    """
    soup = BeautifulSoup(html, "html.parser")

    header_rows = soup.find("table", id="fixedTable")

    for row in header_rows.find_all("tr"):
        cells = row.find_all(["td", "th"])
        row_data = [cell.get_text(strip=True) for cell in cells]
        print(row_data)

    data_rows = soup.find("table", id="scrollTable")

    rows = []

    for row in data_rows.find_all("tr"):
        cells = row.find_all(["td", "th"])
        row_data = [cell.get_text(strip=True) for cell in cells]
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=['Country', 'Year', 'Population below $3.00 a day', 'Population below $4.20 a day', 'Population below $8.30 a day'])

    df = df[~df.eq(NULL_INDICATOR).any(axis=1)]

    # Print the first 5 rows.
    print(df.head())


if __name__ == "__main__":
    print("Fetching HTML...")
    html = fetch_data()

    find_table_parse_df(html)

# This data is useful for comparing poverty levels around the world, 
# however the analysis would likely have to be carefully normalized for inflation as the years the values were aggregated vary by country.
# This is also a very rough, rigid script that I would only use to peek at the data before spending time writing something more
# robust and resistant to changes in the table's html formatting.