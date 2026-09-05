import requests
import json
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 20,
    "page": 1
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

df = pd.DataFrame(data)

df = df[
    ["name", "symbol", "current_price", "market_cap", "total_volume"]
]

print(df.head())

# This dataset contains current market information for cryptocurrencies.
# It includes each cryptocurrency's price, market capitalization, and trading volume.
# I could use these data to compare the largest cryptocurrencies by market value.
# Repeated API calls could help analyze how cryptocurrency prices change over time.