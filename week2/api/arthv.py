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

crypto_data = []

for coin in data:
    crypto_data.append(
        {
            "name": coin["name"],
            "symbol": coin["symbol"],
            "current_price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "total_volume": coin["total_volume"]
        }
    )

df = pd.DataFrame(crypto_data)

print(df.head())

# This dataset contains current market information for cryptocurrencies.
# It includes each cryptocurrency's price, market capitalization, and trading volume.
# I could use these data to compare the largest cryptocurrencies by market value.
# Repeated API calls could help analyze how cryptocurrency prices change over time.