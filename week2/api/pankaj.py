import requests
import json
import pandas as pd 
import os
from dotenv import load_dotenv

# API Key
load_dotenv()
API_KEY = os.getenv("COINGECKO_API_KEY")

# making the request 
url = "https://api.coingecko.com/api/v3/global"
headers = {
    "x-cg-demo-api-key": API_KEY
}

# attaching header information to request 
# storing the request in response
response = requests.get(url, headers=headers)

print(response.status_code)

# parses the JSON response
data = response.json()


# access data and see data fields 
print(data["data"].keys())

# create dictionary of data relative data fields 
crypto_data = {
    "active_cryptocurrencies": data["data"]["active_cryptocurrencies"],
    "markets": data["data"]["markets"],
    "market_cap_change_24h": data["data"]["market_cap_change_percentage_24h_usd"],
    "volume_change_24h": data["data"]["volume_change_percentage_24h_usd"]
}

print(crypto_data)

# create DataFrame
df = pd.DataFrame([crypto_data])
print(df.head())

# This data provides an overview of the global cryptocurrency market.
# It includes the number of active cryptocurrencies and markets.
# It also shows the 24-hour change in market cap and trading volume.
# This data could be used to track changes in the overall crypto market.