from io import StringIO

import requests
import pandas as pd

url = "https://www.scrapethissite.com/pages/forms/?per_page=583"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers).text

table = pd.read_html(StringIO(response))

df = pd.DataFrame(table[0])

print(df.head(5))

# This data has a list of NHL stats since 1990. It has the wins, losses, and win %.
# We could use this data potentially to try and predict wins in the future.
# It might be useful in a ML model to predict teams to likely win based on this past data, or to at least find patterns and find the best teams