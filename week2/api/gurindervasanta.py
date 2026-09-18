import requests
import json
import pandas as pd
import pprint
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CG_API_KEY")
if not api_key:
    raise RuntimeError("CG_API_KEY not set")

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {'ids': 'bitcoin', 'vs_currency': 'usd', 'days': 30}
headers = {"x-cg-demo-api-key": api_key}
response = requests.get(url, params=params, headers=headers)
data = response.json()
df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
# print(df)

vols = []
for obj in data['total_volumes']:
    vols.append(obj[1])
vols = pd.Series(vols)

df['volumes'] = vols
print(df.head())

# NOTE:
# The data gathered here is the price and trading volume of bitcoin cryptocurrency over the last 30 days.
# The timestamp is in the Unix epoch format (milliseconds from Jan 1st 1970), so some conversion might be needed. 
# However, this format would make time arithmetic much simpler. 
# A use case for this data would be to use an LSTM based approach to forecast the prices of bitcoin.