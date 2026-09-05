import requests
import json
import pandas as pd


API_URL = "https://api.coingecko.com/api/v3/coins/markets"  # Public market endpoint.
PARAMS = {  # Requests the ten largest cryptocurrencies in US dollars.
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false",
}

FIELDS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "total_volume",
    "price_change_percentage_24h",
    "last_updated",
]


def build_market_dataframe(records):  # Converts API records into a clean DataFrame.
    """Select and clean useful cryptocurrency market fields."""
    market_df = pd.DataFrame(records)[FIELDS]  # Keeps only the fields needed for analysis.
    market_df = market_df.dropna(subset=["id", "name", "current_price"])
    market_df = market_df.sort_values("market_cap_rank")
    return market_df.reset_index(drop=True)


if __name__ == "__main__":
    response = requests.get(API_URL, params=PARAMS, timeout=30)  # Sends the GET request.
    response.raise_for_status()

    records = json.loads(response.text)  # Parses the JSON response into Python objects.
    market_df = build_market_dataframe(records)
    print(market_df.head())  # Displays the first five rows.

# Notes:
# This dataset contains market data for the ten largest cryptocurrencies by market cap.
# Prices, market cap, and trading volume are reported in US dollars.
# The 24-hour percentage change can be used to compare short-term performance.
# The data could support dashboards, market trend analysis, or investment research.
