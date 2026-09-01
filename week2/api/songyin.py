import requests
import json
import pandas as pd

# CoinGecko API endpoint
url = "https://api.coingecko.com/api/v3/coins/markets"

# Parameters for the API request
params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana"
}

# Make a GET request
response = requests.get(url, params=params)
response.raise_for_status()

# Parse the JSON response
data = response.json()

# Store relevant fields into a DataFrame
df = pd.DataFrame(data)

df = df[
    [
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "price_change_percentage_24h"
    ]
]

# Print the first 5 rows
print(df.head())

# Notes:
# This dataset contains current cryptocurrency market data from CoinGecko.
# It includes names, prices, market capitalization, and 24-hour price changes.
# The data could be used to compare the market performance of cryptocurrencies.
# It could also be used for financial analysis or visualization.