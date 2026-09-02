import requests
import json
import pandas as pd

url = "https://v2.jokeapi.dev/joke/Any"
response = requests.get(url)
data = response.json()

extracted_data = {
    "category": data.get("category"),
    "setup": data.get("setup"),
    "delivery": data.get("delivery"),
}

data = pd.DataFrame([extracted_data])

print(data.head())


#The data from the Joke API is a list of jokes with their respective categories, setups, and deliveries. The API url
#can be edited to filter out certain categories or types of jokes (in order to avoid NSFW content, for example). This data 
#could be used for things like joke generators and sentiment analysis for humor. It can also be useful if you want to train 
#an LLM on jokes or humor for various purposes.
