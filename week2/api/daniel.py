import requests
import json
import pandas as pd

joke_type = input("What type of joke would you like? ")

url = f"https://v2.jokeapi.dev/joke/{joke_type}"

response = requests.get(url)

data = response.json()

# Check whether the API returned an error
if data["error"] == False:

    if data["type"] == "twopart":
        print(data["setup"])
        print(data["delivery"])

    else:
        print(data["joke"])

else:
    print("That is not a valid category!")
