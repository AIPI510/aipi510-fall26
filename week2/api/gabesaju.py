import requests
import json
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}


response = requests.get(url, params=params)
response.raise_for_status()

data = json.loads(response.text)

#pull the fields we care about out of each coin record
records = []
for coin in data:
    record = {
        "name": coin.get("name"),
        "symbol": coin.get("symbol"),
        "price_usd": coin.get("current_price"),
        "market_cap": coin.get("market_cap"),
        "market_cap_rank": coin.get("market_cap_rank"),
    }
    records.append(record)


df = pd.DataFrame(records)
df = df.sort_values(by="market_cap_rank").reset_index(drop=True)

print(df.head())

#Notes
# Source: CoinGecko /coins/markets endpoint
# each row is one cryptocurrency ranked by market cap, with USD price, market cap and market cap rank
# the keyless tier only returns 10 coins regardless of the per_page value
# this is a snapshot from a point in time and not a time series so the values will changes depending on when your run it