import requests
from bs4 import BeautifulSoup
import pandas as pd

# Notes:
# This dataset contains grocery items along with the quantities and prices of each.
# The data was scraped from an HTML table and converted into a pandas DataFrame.
# Quantity and Price were converted from strings into numeric values for analysis as string is not suitable for these features.
# This data could be used to compare prices or calculate costs across different items!

url = "https://www.mth548.org/_static/table.html"

response = requests.get(url)

#ensure url works properly
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

#find first table in the url
table = soup.find("table")

#extract rows
rows = table.find_all("tr")

#formulate data table/set
data = []

#extract cells within each row
for row in rows: 
    cells = row.find_all(["th", "td"])

    row_data = [] #creates a data table for each of the row items to be put in the 'data' table

    for cell in cells:
        row_data.append(cell.get_text(strip=True)) #extract text and remove extra whitespace

    data.append(row_data) #adds the data from the rows into the 'data' table

df = pd.DataFrame(
    data[1:], 
    columns=data[0] #set the first row as the headers
)

df["Quantity"] = pd.to_numeric(df["Quantity"]) #converts string to numeric (quantity)
df["Price"] = df["Price"].str.replace("$", "", regex=False).astype(float) #converts string to float (price)

print(df.head())
print(df.dtypes)
