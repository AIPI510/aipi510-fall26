import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from urllib.parse import urljoin

url = "https://archive.cdc.gov/www_cdc_gov/nchs/nhis/shs/tables.htm"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table") # finds the table with the compiled study tables from various studies

data = []

for row in table.find_all("tr"):
    cells = row.find_all("td")

    if len(cells) == 0:
        continue

    name = cells[0].get_text(strip=True)

    pdf_url = None
    excel_url = None

    for link in row.find_all("a"):
        href = link.get("href")

        if href:
            if href.endswith(".pdf"):
                pdf_url = urljoin(url, href)

            elif href.endswith(".xlsx"):
                excel_url = urljoin(url, href)

#limits pulled data to just name and link to pdf/excel
    data.append({
        "Name": name,
        "PDF": pdf_url,
        "Excel": excel_url
    })

df = pd.DataFrame(data)

# Remove rows without useful links
df = df.dropna(subset=["PDF", "Excel"], how="all")

# Remove duplicates
df = df.drop_duplicates()

# Reset row numbers
df = df.reset_index(drop=True)

# Save the scraped data
df.to_csv("cdc_health_tables.csv", index=False)

# Print first 5 rows
print(df.head())

#scrapes CDC website with tables from various public health studies
#can use this to scrape the site to find studies of interst and compile tables for a ltierature review or presentation
# also provides links to specific pdfs and spreadsheets associated with that study