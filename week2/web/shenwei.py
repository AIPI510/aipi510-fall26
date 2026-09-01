import requests

import pandas as pd
from bs4 import BeautifulSoup


def fetch_table_content_from_url(url: str) -> pd.DataFrame:
    """fetch html content from url
    
    This function gets the html content from a url 
    and returns the first 5 rows as a pandas dataframe.
    If your url has multiple tables, this function will only return the first one.

    Args:
        url (str): The url to fetch the html content from.

    Returns:
        pd.DataFrame: The html content of the url.
    """
    # Send a GET request to the url
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    # Parse the html content using beautiful soup
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Select all rows in the table
    rows = soup.select("table tr")

    # Extract the data from each row
    # and store it in a list of lists
    records = []
    for row in rows:
        cols = row.find_all("td")

        record = []

        for col in cols:
            if col.text.strip():
                record.append(col.text.strip())

        if record:
            records.append(record)

    # Eventually return the first 5 rows as a dataframe
    return pd.DataFrame(records[:5])
