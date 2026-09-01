import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Fetch the webpage content
url = "https://www.basketball-reference.com/leagues/NBA_2026.html"
headers = {"User-Agent": "Mozilla/5.0"}  # Helps prevent getting blocked
response = requests.get(url)

# 2. Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Locate the table
table = soup.find('table')  # Or soup.find("table", class_="my-table-class")

# 4. Extract rows and columns
all_rows = []
for tr in table.find_all("tr"):
    cells = tr.find_all(["td", "th"])
    row_data = [cell.get_text(strip=True) for cell in cells]
    all_rows.append(row_data)

# 5. Load into DataFrame
df = pd.DataFrame(all_rows)
print(df.head(5))

'''
This data shows some data about the NBA Eastern Conference in the 2025-2026 season.
Besides basic win/loss stats, there is also data involving points allowed and points scored.
A basic analysis of these stats combined with off season roster changes could be used to try to predict the standings and point differentials for the upcoming season.
'''