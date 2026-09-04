import sys

import requests
import json
import pandas as pd

# Windows consoles default to cp1252 and cannot print non-ASCII coin names.
sys.stdout.reconfigure(encoding="utf-8")

# CoinGecko's /coins/markets endpoint returns current market data for the top
# coins by market cap. It is free and needs no API key.
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

# Equivalent to response.json(); done this way to use the json library directly.
data = json.loads(response.text)

# The response is a list of dicts, one per coin. Pull out the fields that are
# useful for analysis and drop the rest (image URLs, ROI, redundant deltas).
records = []
for coin in data:
    records.append({
        "rank": coin["market_cap_rank"],
        "id": coin["id"],
        "symbol": coin["symbol"].upper(),
        "name": coin["name"],
        "price_usd": coin["current_price"],
        "market_cap_usd": coin["market_cap"],
        "volume_24h_usd": coin["total_volume"],
        "pct_change_24h": coin["price_change_percentage_24h"],
        "circulating_supply": coin["circulating_supply"],
        "max_supply": coin["max_supply"],
        "all_time_high_usd": coin["ath"],
        "all_time_high_date": coin["ath_date"],
        "last_updated": coin["last_updated"],
    })

df = pd.DataFrame(records)

# --- Cleaning ---

# 1. The API returns timestamps as ISO 8601 strings. Convert them to real
#    datetimes so they can be compared and sorted.
df["all_time_high_date"] = pd.to_datetime(df["all_time_high_date"], format="ISO8601")
df["last_updated"] = pd.to_datetime(df["last_updated"], format="ISO8601")

# 2. max_supply is null for coins with no supply cap (Ethereum, for example).
#    That is a meaningful "no limit", not missing data, so it stays as NaN
#    rather than being filled or dropped.

# 3. Sort by market cap rank so the printed head is the top coins, and drop any
#    coin missing a rank.
df = df.dropna(subset=["rank"]).sort_values("rank").reset_index(drop=True)

print(df.shape)
print(df.head())

# This data is a snapshot of the top 100 cryptocurrencies by market cap, pulled
# from the free CoinGecko /coins/markets API. Each row is one coin, with price,
# market cap, 24h volume, 24h percent change, supply, and all-time-high fields.
# Unlike the NBA data in station 1, this is live and changes every minute, so
# two runs of this script will not produce identical numbers. Any real analysis
# would need to save each pull with its timestamp rather than re-query.
# I kept max_supply as NaN because a null there means the coin has no supply cap
# rather than a missing value, so filling it with 0 would be wrong.
# This could be used to compare volatility across coins, to look at how trading
# volume relates to market cap, or, if collected on a schedule, to build a time
# series for forecasting price movement.
