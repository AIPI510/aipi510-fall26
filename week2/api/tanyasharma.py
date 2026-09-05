# The code fetches cryptocurrency market data from the CoinGecko API and processes it into a pandas DataFrame for analysis.
import requests
import json
import pandas as pd

# Note: I used AI code assist on VSCode for helping guide me with writing this code and fixing debugging issues. 

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINS = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]


# Send a GET request for the selected cryptocurrencies priced in US dollars.
response = requests.get(
	API_URL,
	params={
		"vs_currency": "usd",
		"ids": ",".join(COINS),
		"price_change_percentage": "24h",
	},
	timeout=10,
)
response.raise_for_status()
# Convert the API's JSON response into Python data.
market_data = json.loads(response.text)

# Keep only the market fields needed for the DataFrame.
crypto_records = [
	{
		"name": coin["name"],
		"symbol": coin["symbol"].upper(),
		"current_price_usd": coin["current_price"],
		"market_cap_usd": coin["market_cap"],
		"price_change_24h_percent": coin["price_change_percentage_24h"],
	}
	for coin in market_data
]

# Store the selected records in a table and display the first five rows.
crypto_df = pd.DataFrame(crypto_records)
print(crypto_df.head())


# The data contains current market information for five cryptocurrencies.
# Each row includes the name, symbol, price, market cap, and 24-hour change.
# This dataset could be used to compare cryptocurrency market performance.
# It could also support a market dashboard or price-change alert application.
