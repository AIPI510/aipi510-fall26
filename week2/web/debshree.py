import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Fetch an actual HTML page (Downloads data from a webpage)
url = "https://www.w3schools.com/html/html_tables.asp"
headers_request = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers_request)

# 2. Parse the HTML content from the response (Uses BeautifulSoup)
soup = BeautifulSoup(response.text, "html.parser")

# 3. Locate the table
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

    # Build DataFrame safely (Extracts tabular data into a DataFrame)
    if headers and rows and len(headers) == len(rows[0]):
        df = pd.DataFrame(rows, columns=headers)
    else:
        df = pd.DataFrame(rows)

    # 4. Data-cleaning and filtering step
    # Clean whitespace, drop empty/duplicate rows, and filter for specific countries (e.g., 'Germany')
    df = df.dropna().drop_duplicates()
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Example filter: keep rows where Country is Germany (if Country column exists)
    if "Country" in df.columns:
        filtered_df = df[df["Country"] == "Germany"]
    else:
        filtered_df = df

    # 5. Displays the collected data
    print("--- Extracted and Cleaned Data ---")
    print(filtered_df)

    # 6. Includes at least 3 lines of notes near the bottom
    print("\n--- Notes on Web Scraping Process ---")
    print("1. This script fetches raw HTML from W3Schools and parses the table element using BeautifulSoup.")
    print("2. Extracted text is cleaned by stripping whitespace, removing duplicates, and filtering entries by region.")
    print("3. The final structured dataset is stored in a pandas DataFrame, making it ready for downstream analytical processing.")

else:
    print("No table found on the page.")