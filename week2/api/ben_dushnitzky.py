# AIPI 510 - Week 2, Station 2: Pull Data from an API
# Ben Dushnitzky
# Pulls the top 25 cryptocurrencies by market cap from the CoinGecko public API.
#
# AI use disclosure: I used Claude (Anthropic) to help write and debug this script.

import requests
import json
import pandas as pd

URL = "https://api.coingecko.com/api/v3/coins/markets"

# CoinGecko's public endpoint doesn't need an API key.
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 25,
    "page": 1,
}

response = requests.get(URL, params=params)
print("Status code:", response.status_code)

coins = response.json()
print("Coins returned:", len(coins))

# Print one raw record so I can see what fields the API actually gives back.
print()
print("Example raw record (truncated):")
print(json.dumps(coins[0], indent=2)[:600], "...")
print()

df = pd.DataFrame({
    "name": [c["name"] for c in coins],
    "symbol": [c["symbol"].upper() for c in coins],
    "price_usd": [c["current_price"] for c in coins],
    "market_cap": [c["market_cap"] for c in coins],
    "volume_24h": [c["total_volume"] for c in coins],
    "change_24h_pct": [c["price_change_percentage_24h"] for c in coins],
})

df = df.dropna().reset_index(drop=True)

print("Rows after cleaning:", len(df))
print()
print(df.head())

# Notes on the data:
# Each row is one cryptocurrency in the top 25 by market cap, with its current USD price,
# market cap, 24-hour trading volume, and 24-hour percent price change. This is a live
# snapshot, so re-running the script gives different numbers -- if I polled it on a
# schedule I could build a time series and look at how the coins move relative to each
# other. Volume divided by market cap is also a rough liquidity/turnover measure, and
# the 24h change column makes it easy to see whether the whole market moves together.
