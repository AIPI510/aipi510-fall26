import requests
import json
import pandas as pd

print("Script started")  # ADD THIS

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)  # ADD THIS

data = response.json()
print("Data type:", type(data))  # ADD THIS

df = pd.DataFrame(data)[["id", "symbol", "current_price", "market_cap", "total_volume"]]

print(df.head())