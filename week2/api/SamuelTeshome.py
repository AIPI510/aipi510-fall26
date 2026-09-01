import requests
import json
import pandas as pd

apiURL = "https://healthit.gov/data/open-api?source=aha.csv"

response = requests.get(apiURL)

data = response.json()

df = pd.DataFrame(data)

pd.set_option('display.max_columns', None )

print(df.head(5))

# Pulls Hopsital Certification data on hospitals in every state. Giving an score for percent of hospitals meeting various criteria
# Could use this tool to understand hopspital compliance and how that may influence patient outcomes.