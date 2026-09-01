from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.basketball-reference.com/leagues/NBA_2025_totals.html'


def scrapTable():
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    df = pd.read_html(StringIO(str(table)), flavor="html5lib")[0]
    # All data in correct format
    df.info()
    df = df[df["Rk"].notna()].reset_index(drop=True)
    print(df.head())


if __name__ == "__main__":
    scrapTable()



# All data in correct format - no need to change strs to floats
# Dropping all of the columns where RK is null as these don't have meaningful value

