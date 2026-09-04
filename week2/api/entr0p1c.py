import requests
import json
import pandas as pd

# API endpoint
url = "https://jsonplaceholder.typicode.com/users"

# Send an HTTP GET request
response = requests.get(url)
response.raise_for_status()

# Parse the JSON response
data = response.json()

# Extract selected fields from the API response
records = []

for user in data:
    records.append({
        "id": user["id"],
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
        "city": user["address"]["city"]
    })

# Store the extracted data in a DataFrame
df = pd.DataFrame(records)

# Display the first 5 rows
print("First 5 rows of the dataset:")
print(df.head())

# Notes:
# This API provides sample user information in JSON format.
# The selected fields include user ID, name, username, email, and city.
# The data is stored in a pandas DataFrame for analysis.
# JSONPlaceholder is a free API commonly used for testing and learning.