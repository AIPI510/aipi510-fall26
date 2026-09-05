from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
HEADERS = {
    "User-Agent": (
        "AIPI510 coursework by Yongrong Lu "
        "(https://github.com/AIPI510/aipi510-fall26)"
    )
}


def parse_population_table(html):
    """Parse and clean the main population table from Wikipedia HTML."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="wikitable")

    if table is None:
        raise ValueError("Could not find the population table on the page.")

    population_df = pd.read_html(StringIO(str(table)))[0]
    population_df = population_df.dropna(subset=["Location"])
    population_df = population_df[population_df["Location"] != "Location"]
    return population_df.reset_index(drop=True)


if __name__ == "__main__":
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    population_df = parse_population_table(response.text)
    print(population_df.head())

# Notes:
# This dataset lists countries and dependencies with their latest population estimates.
# It also includes each location's share of world population and the estimate date.
# The data could be used to compare population sizes or identify highly populated regions.
# It could also support demographic visualizations or population-distribution analysis.
