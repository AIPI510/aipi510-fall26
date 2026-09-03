import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Fetch an actual HTML page (not a JSON API endpoint)
url = "https://www.w3schools.com/html/html_tables.asp"
headers_request = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers_request)


# 2. Parse the HTML content from the response
soup = BeautifulSoup(response.text, "html.parser")

# 3. Locate the table (adjust selector to match your target site)
table = soup.find("table")

if table:
    # Extract headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    # Extract rows safely
    rows = []
    tr_elements = (
        table.find("tbody").find_all("tr")
        if table.find("tbody")
        else table.find_all("tr")
    )

    for tr in tr_elements:
        cells = tr.find_all("td")
        if cells:
            rows.append([cell.get_text(strip=True) for cell in cells])

    # Build DataFrame safely
    if headers and rows and len(headers) == len(rows[0]):
        df = pd.DataFrame(rows, columns=headers)
    else:
        df = pd.DataFrame(rows)

    print(df.head())
else:
    print("No table found on the page.")

    '''This code helps us to get the contact details about different people from different regions and to write it in tabular form for further analysis'''

