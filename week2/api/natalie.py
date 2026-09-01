import requests 
from bs4 import BeautifulSoup
import pandas as pd 

import requests

# 1. Define the API endpoint URL
url = "https://v2.jokeapi.dev/joke/Any?amount=10"

# 2. Send the GET request
response = requests.get(url)

# Loop until we successfully collect 5 safe jokes

response = requests.get(url)
print(response.text)

jokes_list = []

if response.status_code == 200:
    data = response.json()
    print(data)
    if isinstance(data, list):
        for joke_data in data:
            jokes_list.append(joke_data["joke"])


# 4. Check if a joke exists and all safety flags are False

    
# 5. Create a DataFrame from the collected safe jokes
print(jokes_list)

#this saves notes for different projects 