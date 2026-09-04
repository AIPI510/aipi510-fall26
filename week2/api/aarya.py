"""Collect public App Store listing metadata from Apple's Search API."""

# %%
import pandas as pd
import requests

API_URL = "https://itunes.apple.com/search"
PARAMS = {
    "term": "habit tracker",
    "country": "us",
    "entity": "software",
    "limit": 15,
}

# Send a GET request using API_URL, PARAMS, and a 30-second timeout.
response = requests.get(API_URL, params=PARAMS, timeout=30)
response.raise_for_status()

# Convert the JSON response into a Python dictionary.
response_data = response.json()

# One API result becomes one row. The first field is completed as an example.
app_records = []
for app in response_data["results"]:
    app_records.append(
        {
            "app_name": app["trackName"],
            "seller": app["sellerName"],
            "category": app["primaryGenreName"],
            "rating": app["averageUserRating"],
            "rating_count": app["userRatingCount"],
            "price": app["price"],
        }
    )
# %%
# Turn app_records into a pandas DataFrame.
apps_df = pd.DataFrame(data=app_records)
apps_df
# %%
# Fill missing ratings with 0 and remove duplicate app names.
apps_df["rating"] = apps_df["rating"].fillna(0)
apps_df = apps_df.drop_duplicates(subset="app_name")

# Sort from the most rating counts to the fewest rating counts.
apps_df = apps_df.sort_values(by="rating_count", ascending=False)

print(apps_df.head(5).to_string(index=False))

# Each row represents an app and how well it is doing.

# You can figure out which apps are best to study within an app category
# by sorting based on rating and rating count.

# Rating and rating count are not foolproof ways to determine an app's
# popularity or financial success. A less popular app (lesser users) may have a
# larger proportion of its users leaving ratings, while another app may have
# fewer ratings but a larger user base. Apple does not publicly disclose the
# number of downloads for an app.
